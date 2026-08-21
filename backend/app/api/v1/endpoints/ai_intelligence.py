from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_reviewer_user, get_current_admin_user
from app.models.user import User
from app.models.question import AICallLog, Question
from app.services.concept_priority_engine import ConceptPriorityEngine
from app.services.ai_question_service import AIQuestionService, QuestionGenerationRequest
from app.services.ai_evaluation_service import AIEvaluationService

router = APIRouter()

class RunEvaluationRequest(BaseModel):
    prompt_version: str = "neetpg-validator-v1.0"
    model_name: str = "medical-validator-v1"
    provider_name: str = "mock"

@router.get("/concept-priority/{concept_id}")
async def get_concept_priority(
    concept_id: str,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluates multi-component high-yield priority score for a concept (Prompt 7, Sec 9).
    """
    return await ConceptPriorityEngine.calculate_concept_priority(db, concept_id)

@router.post("/generate-question", status_code=status.HTTP_201_CREATED)
async def generate_concept_question(
    req: QuestionGenerationRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Concept-driven, evidence-first AI question proposal generator.
    Routes generated question strictly to the Medical Review Queue (NEVER auto-publishes).
    """
    return await AIQuestionService.generate_concept_question_pipeline(
        db=db,
        req=req,
        actor_id=current_user.id
    )

@router.post("/run-evaluation")
async def run_ai_benchmark_evaluation(
    req: RunEvaluationRequest,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Benchmarks AI model and prompt version against fixed gold evaluation dataset (Prompt 7, Sec 44).
    """
    return await AIEvaluationService.run_benchmark_evaluation(
        db=db,
        prompt_version=req.prompt_version,
        model_name=req.model_name,
        provider_name=req.provider_name
    )

@router.get("/observability")
async def get_ai_observability_metrics(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI Observability & Cost Tracking (Prompt 7, Sec 21 & 38).
    """
    stmt_total = select(func.count(AICallLog.id))
    total_calls = (await db.execute(stmt_total)).scalar() or 0

    stmt_tokens = select(func.sum(AICallLog.tokens_prompt + AICallLog.tokens_completion))
    total_tokens = (await db.execute(stmt_tokens)).scalar() or 0

    stmt_cost = select(func.sum(AICallLog.estimated_cost_usd))
    total_cost = (await db.execute(stmt_cost)).scalar() or 0.0

    stmt_success = select(func.count(AICallLog.id)).where(AICallLog.success == True)
    successful_calls = (await db.execute(stmt_success)).scalar() or 0

    stmt_lat = select(func.avg(AICallLog.latency_ms))
    avg_latency = (await db.execute(stmt_lat)).scalar() or 0

    return {
        "total_ai_calls": total_calls,
        "total_tokens_consumed": total_tokens,
        "total_estimated_cost_usd": round(float(total_cost), 4),
        "success_rate_percentage": round((float(successful_calls) / float(total_calls) * 100), 1) if total_calls > 0 else 100.0,
        "avg_latency_ms": round(float(avg_latency), 1)
    }
