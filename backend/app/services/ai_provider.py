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
            estimated_cost_usd=0.00035
        )

class LiveLLMAIProvider(AIProvider):
    """
    Live LLM AI Provider that connects to an external LLM API (OpenAI / Gemini compatible endpoint)
    using settings.AI_API_KEY or OS environment variables.
    """
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        import os
        self.api_key = api_key or getattr(settings, "AI_API_KEY", None) or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.api_base = api_base or os.environ.get("LLM_API_BASE", "https://api.openai.com/v1")

    @property
    def provider_name(self) -> str:
        return "live_llm"

    async def evaluate_question_structured(
        self,
        question_text: str,
        options: list,
        correct_option_key: str,
        explanation: str,
        source_citation: Optional[str] = None,
        model_name: str = "gpt-4o-mini"
    ) -> ProviderExecutionResult:
        import httpx
        start_time = time.time()

        if not self.api_key:
            return ProviderExecutionResult(
                success=False,
                raw_response="",
                error_message="No AI_API_KEY found in settings or environment.",
                latency_ms=0
            )

        prompt = (
            f"You are a Senior Medical Content Inspector for NEET-PG.\n"
            f"Evaluate this medical question for accuracy, ambiguity, and evidence-based standards:\n\n"
            f"Question: {question_text}\n"
            f"Options: {json.dumps(options)}\n"
            f"Correct Key: {correct_option_key}\n"
            f"Explanation: {explanation}\n"
            f"Citation: {source_citation}\n\n"
            f"Respond ONLY in valid JSON matching this exact schema:\n"
            f"{{\n"
            f'  "clinical_accuracy": {{"score": 0.95, "reason": "..."}},\n'
            f'  "single_best_answer": {{"valid": true, "reason": "..."}},\n'
            f'  "ambiguity_risk": {{"score": 0.05, "reason": "..."}},\n'
            f'  "source_support": {{"supported": true, "reason": "..."}},\n'
            f'  "recommendation": "PASS" // or "REVIEW_REQUIRED", "REJECT"\n'
            f"}}\n"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a professional medical exam reviewer."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(f"{self.api_base}/chat/completions", headers=headers, json=payload)
                latency = int((time.time() - start_time) * 1000)

                if res.status_code != 200:
                    return ProviderExecutionResult(
                        success=False,
                        raw_response=res.text,
                        error_message=f"HTTP {res.status_code}: {res.text}",
                        latency_ms=latency
                    )

                data = res.json()
                raw_text = data["choices"][0]["message"]["content"]
                parsed_json = json.loads(raw_text)
                parsed_output = StructuredValidationOutput(**parsed_json)

                tokens_p = data.get("usage", {}).get("prompt_tokens", 0)
                tokens_c = data.get("usage", {}).get("completion_tokens", 0)

                return ProviderExecutionResult(
                    success=True,
                    output=parsed_output,
                    raw_response=raw_text,
                    tokens_prompt=tokens_p,
                    tokens_completion=tokens_c,
                    latency_ms=latency,
                    estimated_cost_usd=(tokens_p * 0.00000015) + (tokens_c * 0.0000006)
                )
        except Exception as exc:
            latency = int((time.time() - start_time) * 1000)
            return ProviderExecutionResult(
                success=False,
                raw_response="",
                error_message=str(exc),
                latency_ms=latency
            )

class AIProviderRegistry:
    _providers: Dict[str, AIProvider] = {
        "mock": MockAIProvider(),
        "live_llm": LiveLLMAIProvider(),
        "openai": LiveLLMAIProvider(),
        "gemini": LiveLLMAIProvider(),
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
