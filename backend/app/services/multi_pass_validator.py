import hashlib
from typing import Dict, Any, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question, QuestionQualityScorecard, AICallLog
from app.services.content_validation_engine import ContentValidationEngine
from app.services.ai_provider import AIProviderRegistry, AIProvider
from app.services.question_lifecycle_service import QuestionLifecycleService
from app.core.datetime_util import utc_now

class MultiPassValidatorService:
    """
    Multi-Pass Medical Validation Pipeline (Prompt 6, Sec 12, 13, 14, 15).
    Executes independent validation passes:
    - Pass 1: Deterministic Single-Best-Answer Check
    - Pass 2: Clinical Vignette Contradiction Check
    - Pass 3: Primary AI Medical Accuracy & Source Check
    - Pass 4: Secondary AI Independent Cross-Check
    - Pass 5: Disagreement & Risk Classification
    """

    @classmethod
    async def run_multi_pass_validation(
        cls,
        db: AsyncSession,
        question_id: str,
        primary_provider_name: str = "mock",
        secondary_provider_name: str = "mock",
        model_name: str = "medical-validator-v1"
    ) -> Dict[str, Any]:
        stmt = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.source),
            selectinload(Question.evidence_references),
            selectinload(Question.quality_scorecard)
        ).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            return {"success": False, "error": "Question not found"}

        options_dict_list = [
            {"option_key": o.option_key, "option_text": o.option_text, "is_correct": o.is_correct}
            for o in question.options
        ]
        correct_key = next((o.option_key for o in question.options if o.is_correct), "A")

        # --- PASS 1: Single Best Answer Check ---
        sba_passed, sba_errors = ContentValidationEngine.validate_single_best_answer(
            options=options_dict_list,
            question_text=question.question_text
        )

        # --- PASS 2: Clinical Vignette Contradiction Check ---
        vignette_passed, vignette_errors = ContentValidationEngine.validate_clinical_vignette(
            question_text=question.question_text
        )

        # --- PASS 3: Primary AI Medical Validation ---
        p1 = AIProviderRegistry.get_provider(primary_provider_name)
        exec1 = await p1.evaluate_question_structured(
            question_text=question.question_text,
            options=options_dict_list,
            correct_option_key=correct_key,
            explanation=question.correct_explanation,
            source_citation=question.source_citation,
            model_name=model_name
        )

        # Log AI Call 1
        call_log1 = AICallLog(
            provider=p1.provider_name,
            model_name=model_name,
            request_type="validation_pass_primary",
            question_id=question.id,
            prompt_hash=hashlib.sha256(question.question_text.encode('utf-8')).hexdigest(),
            tokens_prompt=exec1.tokens_prompt,
            tokens_completion=exec1.tokens_completion,
            latency_ms=exec1.latency_ms,
            estimated_cost_usd=exec1.estimated_cost_usd,
            success=exec1.success,
            error_message=exec1.error_message
        )
        db.add(call_log1)

        # --- PASS 4: Secondary AI Independent Check ---
        p2 = AIProviderRegistry.get_provider(secondary_provider_name)
        exec2 = await p2.evaluate_question_structured(
            question_text=question.question_text,
            options=options_dict_list,
            correct_option_key=correct_key,
            explanation=question.correct_explanation,
            source_citation=question.source_citation,
            model_name=f"{model_name}-cross"
        )

        # Log AI Call 2
        call_log2 = AICallLog(
            provider=p2.provider_name,
            model_name=f"{model_name}-cross",
            request_type="validation_pass_secondary",
            question_id=question.id,
            prompt_hash=hashlib.sha256(question.question_text.encode('utf-8')).hexdigest(),
            tokens_prompt=exec2.tokens_prompt,
            tokens_completion=exec2.tokens_completion,
            latency_ms=exec2.latency_ms,
            estimated_cost_usd=exec2.estimated_cost_usd,
            success=exec2.success,
            error_message=exec2.error_message
        )
        db.add(call_log2)

        # --- PASS 5: Disagreement & Risk Analysis ---
        validator_disagreement = False
        ai_passed = False
        reasons = []

        if not exec1.success or not exec2.success:
            ai_passed = False
            reasons.append("AI validation execution encountered malformed or failed response.")
        elif exec1.output and exec2.output:
            v1_rec = exec1.output.recommendation
            v2_rec = exec2.output.recommendation

            if v1_rec != v2_rec:
                validator_disagreement = True
                ai_passed = False
                reasons.append(f"Validator Disagreement Detected: Provider 1 returned '{v1_rec}' while Provider 2 returned '{v2_rec}'.")
            elif v1_rec == "PASS" and v2_rec == "PASS":
                ai_passed = True
            else:
                ai_passed = False
                reasons.append(f"AI Validators rejected question: {v1_rec}")

        all_passed = sba_passed and vignette_passed and ai_passed and not validator_disagreement

        # Update or Create Quality Scorecard
        scorecard = question.quality_scorecard
        if not scorecard:
            scorecard = QuestionQualityScorecard(question_id=question.id)
            db.add(scorecard)

        scorecard.single_best_answer_passed = sba_passed
        scorecard.clinical_accuracy_passed = vignette_passed and (exec1.output.clinical_accuracy.get("score", 0) > 0.7 if exec1.output else False)
        scorecard.ambiguity_risk_score = exec1.output.ambiguity_risk.get("score", 0.1) if exec1.output else 0.5
        scorecard.overall_quality_score = 0.95 if all_passed else 0.40
        scorecard.validation_report = {
            "sba_passed": sba_passed,
            "sba_errors": sba_errors,
            "vignette_passed": vignette_passed,
            "vignette_errors": vignette_errors,
            "ai_passed": ai_passed,
            "validator_disagreement": validator_disagreement,
            "reasons": reasons,
            "pass_timestamp": utc_now().isoformat()
        }
        scorecard.evaluated_at = utc_now()

        # Update Lifecycle Status according to governance rules
        curr_status = question.status.upper()
        if all_passed:
            # Passes to AI_VALIDATED (Awaiting human medical review before publication)
            if curr_status in ("PROPOSED", "DRAFT"):
                question.status = "AI_VALIDATED"
                question.trust_class = "REVIEW_PENDING"
        else:
            # If any failure or disagreement, routes strictly to REVIEW_REQUIRED
            question.status = "REVIEW_REQUIRED"
            question.trust_class = "REVIEW_PENDING"

        await db.flush()

        return {
            "question_id": question.id,
            "all_passed": all_passed,
            "single_best_answer_passed": sba_passed,
            "vignette_passed": vignette_passed,
            "ai_passed": ai_passed,
            "validator_disagreement": validator_disagreement,
            "status": question.status,
            "trust_class": question.trust_class,
            "errors": sba_errors + vignette_errors + reasons
        }
