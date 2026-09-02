import asyncio
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.question import Question, QuestionOption


async def main():
    async with AsyncSessionLocal() as db:
        # 1. Correct-answer-key distribution
        stmt = (
            select(QuestionOption.option_key, func.count())
            .where(QuestionOption.is_correct == True)
            .group_by(QuestionOption.option_key)
        )
        rows = (await db.execute(stmt)).all()
        total = sum(c for _, c in rows)
        print("=== Correct-answer-key distribution (LIVE, right now) ===")
        for key, count in sorted(rows):
            pct = (count / total * 100) if total else 0
            print(f"  Option {key}: {count} ({pct:.1f}%)")
        print(f"  Total published questions with a correct option: {total}")
        print()

        # 2. Template check — how many questions still literally contain
        #    the placeholder marker
        stmt2 = select(func.count()).select_from(Question).where(
            Question.question_text.like("%CANDIDATE #%")
        )
        template_count = (await db.execute(stmt2)).scalar_one()
        print(f"=== Questions still containing '[SUBJ CANDIDATE #idx]' template marker: {template_count} ===")
        print()

        # 3. Sample raw question text
        stmt3 = select(Question.question_text).limit(5)
        samples = (await db.execute(stmt3)).scalars().all()
        print("=== Sample of 5 raw question_text values ===")
        for i, s in enumerate(samples, 1):
            print(f"{i}. {s[:200]}")


if __name__ == "__main__":
    asyncio.run(main())
