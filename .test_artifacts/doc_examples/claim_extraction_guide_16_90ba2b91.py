# Example from: docs\tools\claim_extraction_guide.md
# Index: 16
# Runnable: False
# Hash: 90ba2b91

def assign_priority(claim: Dict) -> str:
    # Example: Treat all controller claims as HIGH
    if "controller" in claim["file"].lower():
        return "HIGH"

    # Original logic...
    if claim["type"] in ["theorem", "lemma"] and claim["confidence"] < 0.8:
        return "CRITICAL"