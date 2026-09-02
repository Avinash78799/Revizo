import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

async def seed_full_corpus():
    print("="*80)
    print("CRITICAL SECURITY & GOVERNANCE NOTICE")
    print("Scripted auto-approval of candidate questions via hardcoded loops is DEPRECATED.")
    print("All content publication and verification must go through either:")
    print(" 1) Real human medical reviewer sign-off via the Medical Reviewer Portal, or")
    print(" 2) Automated multi-pass validation pipeline (multi_pass_validator.py).")
    print("="*80)
    raise RuntimeError(
        "Scripted auto-approval disabled. "
        "Questions must pass multi_pass_validator.py or receive authentic medical reviewer sign-off before being published or tagged as verified."
    )

if __name__ == "__main__":
    try:
        asyncio.run(seed_full_corpus())
    except RuntimeError as e:
        print(f"\n[GOVERNANCE GATE] {e}")
