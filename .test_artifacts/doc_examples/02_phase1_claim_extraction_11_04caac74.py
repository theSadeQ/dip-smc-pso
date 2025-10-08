# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 11
# Runnable: False
# Hash: 04caac74

def assign_priority(claim: Dict) -> str:
    """
    CRITICAL: Uncited formal theorems/lemmas (scientific risk)
    HIGH: Uncited implementation claims (reproducibility risk)
    MEDIUM: Already cited OR informal claims
    """

    if (claim.get('category') == 'theoretical' and
        claim.get('type') in ['theorem', 'lemma', 'proposition'] and
        not claim.get('has_citation')):
        return 'CRITICAL'  # ~29 claims

    if (claim.get('category') == 'implementation' and
        not claim.get('has_citation')):
        return 'HIGH'  # ~136 claims

    return 'MEDIUM'  # ~335 claims