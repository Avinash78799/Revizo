import asyncio
import hashlib
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import (
    User, Profile, Subject, Chapter, Topic, Concept,
    Source, SourceVersion, PyqReference, Question, QuestionOption,
    QuestionQualityScorecard, TestTemplate
)

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()

async def _seed_data(session: AsyncSession):
    # Check if already seeded
    existing_user = await session.execute(select(User))
    if existing_user.scalars().first():
        return

    # 1. Create Default Development Users
    demo_student = User(
        email="aspirant@neetpg.pro",
        hashed_password=get_password_hash("Password123!"),
        role="student",
        is_active=True
    )
    session.add(demo_student)
    await session.flush()

    student_profile = Profile(
        user_id=demo_student.id,
        full_name="Dr. Aspirant [DEVELOPMENT SEED]",
        target_exam_year=2026,
        daily_question_goal=10
    )
    session.add(student_profile)

    demo_admin = User(
        email="admin@neetpg.pro",
        hashed_password=get_password_hash("AdminSecure123!"),
        role="admin",
        is_active=True
    )
    session.add(demo_admin)
    await session.flush()

    admin_profile = Profile(
        user_id=demo_admin.id,
        full_name="Chief Medical Admin [DEVELOPMENT SEED]",
        daily_question_goal=0
    )
    session.add(admin_profile)

    # 2. Sources Registry (Marked explicitly with provenance)
    src_kdt = Source(
        title="Essentials of Medical Pharmacology [DEVELOPMENT SEED REFERENCE]",
        publisher="Jaypee Brothers Medical Publishers",
        source_type="standard_textbook",
        edition_or_year="8th Edition",
        reference_identifier="ISBN 978-9352704996",
        license_status="reference_only",
        notes="Standard pharmacological reference. Tagged as development benchmark reference."
    )
    src_robbins = Source(
        title="Robbins and Cotran Pathologic Basis of Disease [DEVELOPMENT SEED REFERENCE]",
        publisher="Elsevier",
        source_type="standard_textbook",
        edition_or_year="10th Edition",
        reference_identifier="ISBN 978-0323531139",
        license_status="reference_only",
        notes="Standard pathological reference. Tagged as development benchmark reference."
    )
    session.add_all([src_kdt, src_robbins])
    await session.flush()

    # 3. Subject 1: Pharmacology
    sub_pharm = Subject(name="Pharmacology", code="PHARM", description="General & Systemic Pharmacology", order_index=1)
    session.add(sub_pharm)
    await session.flush()

    chap_ans = Chapter(subject_id=sub_pharm.id, name="Autonomic Nervous System", order_index=1)
    session.add(chap_ans)
    await session.flush()

    top_cholinergic = Topic(chapter_id=chap_ans.id, name="Cholinergic System & Anticholinesterases", order_index=1)
    session.add(top_cholinergic)
    await session.flush()

    # 4. Subject 2: Pathology
    sub_path = Subject(name="Pathology", code="PATH", description="General & Systemic Pathology", order_index=2)
    session.add(sub_path)
    await session.flush()

    chap_cell = Chapter(subject_id=sub_path.id, name="General Pathology: Cell Injury & Adaptation", order_index=1)
    session.add(chap_cell)
    await session.flush()

    top_necrosis = Topic(chapter_id=chap_cell.id, name="Patterns of Tissue Necrosis", order_index=1)
    session.add(top_necrosis)
    await session.flush()

    # 5. Create 25 Verified SOURCE_REFERENCED Questions
    for i in range(1, 26):
        target_topic = top_cholinergic if i <= 15 else top_necrosis
        target_source = src_kdt if i <= 15 else src_robbins

        concept = Concept(
            topic_id=target_topic.id,
            name=f"High-Yield Clinical Concept #{i}",
            high_yield_notes=f"Key clinical facts for concept #{i}.",
            clinical_pearl=f"High-yield takeaway pearl for #{i}.",
            exam_relevance_score=0.95
        )
        session.add(concept)
        await session.flush()

        q_text = (
            f"A patient presents with classic clinical findings related to medical concept #{i}. "
            "After thorough initial diagnostic workup and laboratory investigations, which of the following "
            "represents the single best next step or correct pharmacological/pathological characteristic?"
        )
        q = Question(
            concept_id=concept.id,
            trust_class="SOURCE_REFERENCED",
            question_type="clinical_vignette",
            difficulty="moderate",
            status="published",
            is_high_yield=True,
            question_text=q_text,
            correct_explanation=f"Option B is correct based on standard medical textbook principles for concept #{i}.",
            remember_takeaway=f"High-yield takeaway pearl for concept #{i}.",
            exam_connection="High-yield core exam concept.",
            detailed_explanation=f"Comprehensive textbook breakdown for concept #{i}.",
            source_id=target_source.id,
            source_citation=f"Standard Medical Textbook Reference, 10th Ed, Chapter {i}, p. 100-110.",
            is_ai_generated=False,
            text_hash=compute_hash(q_text)
        )
        session.add(q)
        await session.flush()

        session.add_all([
            QuestionOption(question_id=q.id, option_key="A", option_text="Initial incorrect option", is_correct=False, why_wrong_explanation="Incorrect distractor."),
            QuestionOption(question_id=q.id, option_key="B", option_text="Verified correct therapeutic step", is_correct=True, why_wrong_explanation=None),
            QuestionOption(question_id=q.id, option_key="C", option_text="Alternative incorrect option", is_correct=False, why_wrong_explanation="Incorrect distractor."),
            QuestionOption(question_id=q.id, option_key="D", option_text="Contraindicated intervention", is_correct=False, why_wrong_explanation="Incorrect distractor.")
        ])

        session.add(QuestionQualityScorecard(
            question_id=q.id,
            medical_accuracy_passed=True,
            syllabus_alignment_passed=True,
            single_best_answer_passed=True,
            ambiguity_flag=False,
            source_verified=True,
            overall_quality_score=1.0,
            validation_report={"status": "source_verified", "validator": "expert_review"}
        ))

    # 6. Default Test Templates
    session.add_all([
        TestTemplate(
            title="Daily Quick Test (10 Questions)",
            mode="quick_test",
            config={"question_count": 10, "time_limit_minutes": 10, "allow_confidence": True}
        ),
        TestTemplate(
            title="Topic Practice Sprint (15 Questions)",
            mode="topic_test",
            config={"question_count": 15, "time_limit_minutes": 15, "allow_confidence": True}
        ),
        TestTemplate(
            title="Chapter Revision Test (20 Questions)",
            mode="chapter_test",
            config={"question_count": 20, "time_limit_minutes": 25, "allow_confidence": True}
        )
    ])

    await session.commit()

async def seed_database(session: Optional[AsyncSession] = None):
    """Seed entrypoint accepting an optional session."""
    if session is not None:
        await _seed_data(session)
    else:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSessionLocal() as s:
            await _seed_data(s)

if __name__ == "__main__":
    asyncio.run(seed_database())
