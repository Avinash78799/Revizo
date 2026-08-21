from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.db.seed import seed_database
from app.api.v1.router import api_router
from app.core.errors import AppError, AuthorizationError, AuthenticationError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed development taxonomy on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Free, trustworthy, AI-assisted NEET-PG practice & revision platform API.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized Error Envelopes (No stack traces or secrets exposed to clients)
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(l) for l in err.get("loc", [])])
        errors.append({"location": loc, "message": err.get("msg")})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Request validation failed.", "details": {"validation_errors": errors}}}
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log internal traceback on server console, return generic 500 to client
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred. Please try again later."}}
    )

# Health and Readiness Endpoints
@app.get("/health", tags=["Health & Readiness"])
async def health():
    """Liveness probe: verifies application server is active."""
    return {"status": "healthy", "service": "neet-pg-api", "version": "1.0.0"}

@app.get("/ready", tags=["Health & Readiness"])
async def readiness():
    """Readiness probe: verifies database connectivity safely."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unavailable", "message": "Database connectivity check failed."}
        )

# Mount API v1 Master Router
app.include_router(api_router, prefix=settings.API_V1_STR)
