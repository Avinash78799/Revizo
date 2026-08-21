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

    concept_op = Concept(
        topic_id=top_cholinergic.id,
        name="Organophosphate Poisoning: Mechanism & Management with Atropine vs Pralidoxime",
        high_yield_notes="OP compounds irreversibly phosphorylate and inactivate acetylcholinesterase, leading to massive acetylcholine buildup at both muscarinic and nicotinic synapses.",
        clinical_pearl="Atropine reverses life-threatening muscarinic signs (bronchorrhea, bradycardia); Pralidoxime (2-PAM) reactivates phosphorylated acetylcholinesterase if given before aging.",
        exam_relevance_score=0.98
    )
    concept_mg = Concept(
        topic_id=top_cholinergic.id,
        name="Myasthenia Gravis: Pathophysiology and Maintenance Therapy with Pyridostigmine",
        high_yield_notes="Autoimmune disorder caused by anti-nicotinic acetylcholine receptor (AChR) antibodies at the post-synaptic neuromuscular junction membrane.",
        clinical_pearl="Pyridostigmine is the drug of choice for maintenance; Edrophonium (Tensilon) is ultra-short acting and used for diagnostic testing.",
        exam_relevance_score=0.95
    )
    session.add_all([concept_op, concept_mg])
    await session.flush()

    # Question 1: Explicitly tagged trust_class = "development_seed"
    q1_text = (
        "[DEVELOPMENT SEED QUESTION] A 32-year-old agricultural worker is brought to the emergency department in severe respiratory distress "
        "after spraying crops without protective gear. Physical examination reveals pinpoint pupils, marked salivation, diaphoresis, "
        "diffuse bilateral wheezing, and muscle fasciculations. His pulse is 48 beats/min and blood pressure is 94/58 mmHg. "
        "Which of the following is the most appropriate immediate drug to reverse his life-threatening respiratory symptoms?"
    )
    q1 = Question(
        concept_id=concept_op.id,
        trust_class="development_seed",  # Isolated from verified production pool
        question_type="clinical_vignette",
        difficulty="moderate",
        status="published",
        is_high_yield=True,
        question_text=q1_text,
        correct_explanation="Atropine is a competitive muscarinic antagonist and the primary life-saving antidote for organophosphate poisoning. It immediately reverses life-threatening muscarinic manifestations—specifically bronchoconstriction, excessive tracheobronchial secretions (bronchorrhea), and bradycardia.",
        remember_takeaway="Atropine blocks lethal muscarinic hyperstimulation (bronchorrhea and bradycardia); Pralidoxime (2-PAM) reactivates phosphorylated acetylcholinesterase before chemical aging.",
        exam_connection="High-yield toxicology concept in emergency pharmacology.",
        detailed_explanation="Organophosphates phosphorylate the esteratic site of acetylcholinesterase, causing acetylcholine accumulation at muscarinic and nicotinic receptors. Atropine crosses the blood-brain barrier for central and peripheral muscarinic effects, but has NO effect at nicotinic neuromuscular junctions.",
        source_id=src_kdt.id,
        source_citation="K.D. Tripathi, Essentials of Medical Pharmacology, 8th Ed, Ch. 7, p. 112-116.",
        is_ai_generated=False,
        text_hash=compute_hash(q1_text)
    )
    session.add(q1)
    await session.flush()

    session.add_all([
        QuestionOption(question_id=q1.id, option_key="A", option_text="Physostigmine", is_correct=False, why_wrong_explanation="Physostigmine is itself an acetylcholinesterase inhibitor (used for atropine toxicity). Administering it here would further inhibit cholinesterase and worsen toxicity."),
        QuestionOption(question_id=q1.id, option_key="B", option_text="Atropine sulfate", is_correct=True, why_wrong_explanation=None),
        QuestionOption(question_id=q1.id, option_key="C", option_text="Neostigmine", is_correct=False, why_wrong_explanation="Neostigmine is a reversible anticholinesterase that would aggravate cholinergic hyperstimulation."),
        QuestionOption(question_id=q1.id, option_key="D", option_text="Pilocarpine", is_correct=False, why_wrong_explanation="Pilocarpine is a direct-acting muscarinic agonist that would worsen bronchospasm, secretions, and bradycardia.")
    ])

    session.add(QuestionQualityScorecard(
        question_id=q1.id,
        medical_accuracy_passed=True,
        syllabus_alignment_passed=True,
        single_best_answer_passed=True,
        ambiguity_flag=False,
        source_verified=True,
        overall_quality_score=1.0,
        validation_report={"status": "development_seed_verified", "validator": "manual_development_seed"}
    ))

    # Question 2: Explicitly tagged trust_class = "development_seed"
    q2_text = (
        "[DEVELOPMENT SEED QUESTION] A 28-year-old woman presents with fluctuating bilateral ptosis, diplopia, and generalized muscle fatigue "
        "that worsens towards the evening. An edrophonium (Tensilon) test results in rapid, transient improvement of muscle strength. "
        "Which of the following is the most appropriate first-line oral agent for long-term symptomatic maintenance therapy?"
    )
    q2 = Question(
        concept_id=concept_mg.id,
        trust_class="development_seed",
        question_type="clinical_vignette",
        difficulty="moderate",
        status="published",
        is_high_yield=True,
        question_text=q2_text,
        correct_explanation="Pyridostigmine is the first-line oral anticholinesterase for symptomatic maintenance therapy of Myasthenia Gravis. It has an intermediate duration of action (4-6 hours), fewer muscarinic side effects, and better gastrointestinal tolerance than neostigmine.",
        remember_takeaway="Pyridostigmine (oral, 4-6h duration) is the drug of choice for long-term maintenance in Myasthenia Gravis; Edrophonium is ultra-short-acting (5-10 min) and used for diagnosis.",
        exam_connection="Distinguishing myasthenic crisis from cholinergic crisis is high-yield in neurology/pharmacology.",
        detailed_explanation="Myasthenia Gravis involves autoantibodies against post-synaptic nicotinic ACh receptors. Anticholinesterases prevent acetylcholine degradation in the synaptic cleft, increasing receptor occupancy.",
        source_id=src_kdt.id,
        source_citation="K.D. Tripathi, Essentials of Medical Pharmacology, 8th Ed, Ch. 7, p. 110-111.",
        is_ai_generated=False,
        text_hash=compute_hash(q2_text)
    )
    session.add(q2)
    await session.flush()

    session.add_all([
        QuestionOption(question_id=q2.id, option_key="A", option_text="Pyridostigmine", is_correct=True, why_wrong_explanation=None),
        QuestionOption(question_id=q2.id, option_key="B", option_text="Succinylcholine", is_correct=False, why_wrong_explanation="Succinylcholine is a depolarizing neuromuscular blocker and would precipitate profound, life-threatening paralysis in myasthenia patients."),
        QuestionOption(question_id=q2.id, option_key="C", option_text="Atropine", is_correct=False, why_wrong_explanation="Atropine is an antimuscarinic agent; it has no therapeutic action on nicotinic receptors at the skeletal neuromuscular junction."),
        QuestionOption(question_id=q2.id, option_key="D", option_text="Pralidoxime", is_correct=False, why_wrong_explanation="Pralidoxime is a cholinesterase reactivator used specifically in organophosphate poisoning; it has no efficacy against autoimmune receptor loss.")
    ])

    session.add(QuestionQualityScorecard(
        question_id=q2.id,
        medical_accuracy_passed=True,
        syllabus_alignment_passed=True,
        single_best_answer_passed=True,
        ambiguity_flag=False,
        source_verified=True,
        overall_quality_score=1.0,
        validation_report={"status": "development_seed_verified", "validator": "manual_development_seed"}
    ))

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

    concept_necrosis = Concept(
        topic_id=top_necrosis.id,
        name="Liquefactive vs Coagulative Necrosis in Hypoxic Ischemic Tissue",
        high_yield_notes="Coagulative necrosis preserves underlying tissue architecture for days (ghost cells); Liquefactive necrosis completely digests tissue into a viscous liquid mass.",
        clinical_pearl="Hypoxic infarction of solid organs (heart, kidney, spleen) causes coagulative necrosis; hypoxic infarction of the brain (CNS) characteristically produces liquefactive necrosis.",
        exam_relevance_score=0.96
    )
    session.add(concept_necrosis)
    await session.flush()

    q3_text = (
        "[DEVELOPMENT SEED QUESTION] A 68-year-old man with a history of atrial fibrillation suffers an acute ischemic stroke with right-sided hemiplegia. "
        "He passes away 6 days later from aspiration pneumonia. Autopsy examination of the cerebral hemisphere reveals a focal softened, "
        "cystic area containing cellular debris and lipid-laden microglial cells. Which pattern of necrosis is most characteristic of this lesion?"
    )
    q3 = Question(
        concept_id=concept_necrosis.id,
        trust_class="development_seed",
        question_type="clinical_vignette",
        difficulty="moderate",
        status="published",
        is_high_yield=True,
        question_text=q3_text,
        correct_explanation="Ischemic stroke (hypoxic injury) in the central nervous system (CNS) characteristically results in liquefactive necrosis due to high lipid content, rich release of lysosomal hydrolytic enzymes from microglial cells, and lack of a robust fibrous extracellular matrix framework.",
        remember_takeaway="Hypoxic infarction in the Brain (CNS) causes Liquefactive Necrosis, whereas infarction in all other solid organs (Heart, Kidney, Spleen) causes Coagulative Necrosis.",
        exam_connection="Classic high-yield general pathology concept.",
        detailed_explanation="In liquefactive necrosis, enzymatic digestion of dead cells transforms tissue into a liquid viscous mass. Coagulative necrosis is typical of infarcts in solid organs where protein denaturation predominates.",
        source_id=src_robbins.id,
        source_citation="Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Ch. 2, p. 41-43.",
        is_ai_generated=False,
        text_hash=compute_hash(q3_text)
    )
    session.add(q3)
    await session.flush()

    session.add_all([
        QuestionOption(question_id=q3.id, option_key="A", option_text="Coagulative necrosis", is_correct=False, why_wrong_explanation="Coagulative necrosis occurs with ischemia in solid organs (myocardium, kidney), but the brain is a notable exception due to abundant lysosomal enzymes leading to liquefaction."),
        QuestionOption(question_id=q3.id, option_key="B", option_text="Liquefactive necrosis", is_correct=True, why_wrong_explanation=None),
        QuestionOption(question_id=q3.id, option_key="C", option_text="Caseous necrosis", is_correct=False, why_wrong_explanation="Caseous necrosis ('cheese-like') is characteristic of tuberculous granulomas and fungal infections, not acute cerebral infarction."),
        QuestionOption(question_id=q3.id, option_key="D", option_text="Fibrinoid necrosis", is_correct=False, why_wrong_explanation="Fibrinoid necrosis is seen in immune complex-mediated vasculitis (e.g., Polyarteritis Nodosa) and malignant hypertension affecting arterial walls.")
    ])

    session.add(QuestionQualityScorecard(
        question_id=q3.id,
        medical_accuracy_passed=True,
        syllabus_alignment_passed=True,
        single_best_answer_passed=True,
        ambiguity_flag=False,
        source_verified=True,
        overall_quality_score=1.0,
        validation_report={"status": "development_seed_verified", "validator": "manual_development_seed"}
    ))

    # 5. Default Test Templates
    session.add_all([
        TestTemplate(
            title="Daily Quick Test (5 Questions)",
            mode="quick_test",
            config={"question_count": 5, "time_limit_minutes": 5, "allow_confidence": True}
        ),
        TestTemplate(
            title="Topic Practice Sprint (10 Questions)",
            mode="topic_test",
            config={"question_count": 10, "time_limit_minutes": 10, "allow_confidence": True}
        ),
        TestTemplate(
            title="5-Minute High-Yield Revision",
            mode="five_minute_revision",
            config={"question_count": 5, "time_limit_minutes": 5, "allow_confidence": True}
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
