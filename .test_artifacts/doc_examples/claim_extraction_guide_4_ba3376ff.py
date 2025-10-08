# Example from: docs\tools\claim_extraction_guide.md
# Index: 4
# Runnable: False
# Hash: ba3376ff

# example-metadata:
# runnable: false

def assign_priority(claim: Dict) -> str:
    """Priority assignment based on claim attributes."""

    # Rule 1: Formal theorems/lemmas without citations → CRITICAL
    if claim["type"] in ["theorem", "lemma"] and claim["confidence"] < 0.8:
        return "CRITICAL"

    # Rule 2: Code implementations without specific sources → HIGH
    if claim["source"] == "code" and claim["confidence"] < 0.7:
        return "HIGH"

    # Rule 3: Already cited (confidence ≥0.8) → MEDIUM
    if claim["confidence"] >= 0.8:
        return "MEDIUM"

    # Rule 4: Informal or supporting claims → MEDIUM
    if claim["type"] in ["proposition", "note", "remark"]:
        return "MEDIUM"

    # Default: MEDIUM
    return "MEDIUM"