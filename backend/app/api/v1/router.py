from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    taxonomy,
    test,
    questions,
    revision,
    student,
    admin,
    reports,
    governance,
    ai_intelligence,
    historical_patterns
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(taxonomy.router, prefix="/taxonomy", tags=["Curriculum Taxonomy"])
api_router.include_router(test.router, prefix="/test", tags=["Practice & Tests (Legacy)"])
api_router.include_router(test.router, prefix="/tests", tags=["Practice & Tests"])
api_router.include_router(questions.router, prefix="/questions", tags=["Student Questions & Reports"])
api_router.include_router(revision.router, prefix="/revision", tags=["Spaced Revision"])
api_router.include_router(student.router, prefix="/student", tags=["Student Intelligence"])
api_router.include_router(student.router, prefix="", tags=["Dashboard Root"])
api_router.include_router(historical_patterns.router, prefix="/historical-patterns", tags=["PYQ Patterns & Recall Analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin & Review Queue"])
api_router.include_router(reports.router, prefix="/reports", tags=["Question Reports"])
api_router.include_router(reports.router, prefix="/governance", tags=["Question Reports (Governance Alias)"])
api_router.include_router(governance.router, prefix="/admin/governance", tags=["Content Governance & Quality"])
api_router.include_router(ai_intelligence.router, prefix="/admin/ai", tags=["AI Question Intelligence"])
