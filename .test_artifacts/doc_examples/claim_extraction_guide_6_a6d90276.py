# Example from: docs\tools\claim_extraction_guide.md
# Index: 6
# Runnable: False
# Hash: a6d90276

# example-metadata:
# runnable: false

def test_ground_truth_recall():
    # Ground truth: docs/theory/smc_theory_complete.md
    expected_claims = [
        "Theorem 1: Sliding surface convergence",
        "Lemma 2: Boundary layer stability",
        # ... (manually verified, 18 total)
    ]

    extractor = FormalExtractor()
    extracted = extractor.extract("docs/theory/smc_theory_complete.md")

    recall = len(extracted) / len(expected_claims)
    assert recall >= 0.95, f"Recall {recall:.2%} below target 95%"