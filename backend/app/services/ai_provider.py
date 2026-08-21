import json
import time
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.question import AICallLog
from app.core.config import settings
from app.core.errors import ProviderUnavailableError

class StructuredValidationOutput(BaseModel):
    clinical_accuracy: Dict[str, Any] = Field(..., description="{'score': float, 'reason': str}")
    single_best_answer: Dict[str, Any] = Field(..., description="{'valid': bool, 'reason': str}")
    ambiguity_risk: Dict[str, Any] = Field(..., description="{'score': float, 'reason': str}")
    source_support: Dict[str, Any] = Field(..., description="{'supported': bool, 'reason': str}")
    recommendation: str = Field(..., description="'PASS', 'REVIEW_REQUIRED', 'REJECT'")

class AIProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    async def evaluate_question_structured(
        self,
        question_text: str,
        options: list,
        correct_option_key: str,
        explanation: str,
        source_citation: Optional[str] = None,
        model_name: str = "medical-validator-v1"
    ) -> ProviderExecutionResult:
        pass

# Return type for provider executions
class ProviderExecutionResult(BaseModel):
    success: bool
    output: Optional[StructuredValidationOutput] = None
    raw_response: str
    tokens_prompt: int = 0
    tokens_completion: int = 0
    latency_ms: int = 0
    estimated_cost_usd: float = 0.0
    error_message: Optional[str] = None

class MockAIProvider(AIProvider):
    """
    Deterministic Mock AI Provider for testing and local validation without external network dependencies.
    Supports injecting simulated malformed outputs or disagreements.
    """
    def __init__(self, simulate_malformed: bool = False, force_verdict: Optional[str] = None):
        self.simulate_malformed = simulate_malformed
        self.force_verdict = force_verdict

    @property
    def provider_name(self) -> str:
        return "mock"

    async def evaluate_question_structured(
        self,
        question_text: str,
        options: list,
        correct_option_key: str,
        explanation: str,
        source_citation: Optional[str] = None,
        model_name: str = "mock-medical-validator"
    ) -> ProviderExecutionResult:
        start_time = time.time()

        if self.simulate_malformed:
            return ProviderExecutionResult(
                success=False,
                raw_response="Unparseable non-JSON text: The medical question looks fine but...",
                error_message="JSONDecodeError: Expecting value: line 1 column 1",
                latency_ms=10,
                tokens_prompt=120,
                tokens_completion=25,
                estimated_cost_usd=0.0001
            )

        verdict = self.force_verdict or "PASS"

        result_payload = {
            "clinical_accuracy": {
                "score": 0.95 if verdict == "PASS" else 0.40,
                "reason": "Standard pharmacotherapeutic guidelines verified."
            },
            "single_best_answer": {
                "valid": verdict != "REJECT",
                "reason": "Clear unambiguous best answer identified."
            },
            "ambiguity_risk": {
                "score": 0.05 if verdict == "PASS" else 0.85,
                "reason": "Distractors are mutually distinct."
            },
            "source_support": {
                "supported": True,
                "reason": "Source reference aligned with standard medical curricula."
            },
            "recommendation": verdict
        }

        latency = int((time.time() - start_time) * 1000)
        parsed = StructuredValidationOutput(**result_payload)

        return ProviderExecutionResult(
            success=True,
            output=parsed,
            raw_response=json.dumps(result_payload),
            tokens_prompt=250,
            tokens_completion=90,
            latency_ms=max(1, latency),
            estimated_cost_usd=0.00035
        )

class AIProviderRegistry:
    _providers: Dict[str, AIProvider] = {
        "mock": MockAIProvider(),
    }

    @classmethod
    def get_provider(cls, name: str = "mock") -> AIProvider:
        # Strict Fail-Closed Rule for Production (Milestone 5.1 Hardening)
        is_production = getattr(settings, "ENVIRONMENT", "development").lower() == "production"
        allow_mock = getattr(settings, "ALLOW_MOCK_AI", True)

        if name.lower() == "mock" and is_production and not allow_mock:
            raise ProviderUnavailableError("mock", "Mock AI Provider is strictly forbidden in production mode.")

        provider = cls._providers.get(name.lower())
        if not provider:
            if is_production or not allow_mock:
                raise ProviderUnavailableError(name, f"AI Provider '{name}' is not registered or unavailable. Mock fallback is strictly forbidden in production.")
            # Only in non-production development/test mode allows fallback
            return cls._providers["mock"]
        return provider

    @classmethod
    def register_provider(cls, name: str, provider: AIProvider):
        cls._providers[name.lower()] = provider
