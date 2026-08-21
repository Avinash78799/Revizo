from typing import Dict, Any

class FeatureFlagService:
    """
    Milestone 10 Beta Dynamic Feature Flags (Prompt 14, Sec 14).
    Enables disabling experimental features without code redeployment.
    """

    _FLAGS: Dict[str, bool] = {
        "AI_QUESTION_GENERATION": True,
        "EXPERIMENTAL_RECOMMENDER": True,
        "ADVANCED_ANALYTICS": True,
        "STRICT_INTEGRITY_ENFORCEMENT": True,
        "MICRO_REVISION_MODES": True,
        "PUBLIC_SIGNUP_OPEN": False  # Beta restriction
    }

    @classmethod
    def is_enabled(cls, flag_name: str) -> bool:
        return cls._FLAGS.get(flag_name, False)

    @classmethod
    def set_flag(cls, flag_name: str, enabled: bool) -> None:
        cls._FLAGS[flag_name] = enabled

    @classmethod
    def get_all_flags(cls) -> Dict[str, bool]:
        return dict(cls._FLAGS)
