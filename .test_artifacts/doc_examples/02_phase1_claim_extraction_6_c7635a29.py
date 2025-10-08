# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 6
# Runnable: False
# Hash: c7635a29

def test_extract_numbered_theorem():
    text = """
    **Theorem 1** (Convergence)

    The system converges in finite time.

    **Proof**: Trivial. □
    """

    claims = extractor.extract_from_text(text)

    assert len(claims) == 1
    assert claims[0].type == "theorem"
    assert claims[0].number == 1
    assert claims[0].proof is not None
    assert claims[0].confidence >= 0.8

def test_citation_detection():
    text = """
    **Theorem 2** {cite}`levant2003higher`

    Super-twisting guarantees convergence.
    """

    claims = extractor.extract_from_text(text)
    assert claims[0].has_citation == True
    assert claims[0].confidence >= 0.9