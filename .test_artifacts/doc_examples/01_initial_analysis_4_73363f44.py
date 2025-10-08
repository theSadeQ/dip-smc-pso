# Example from: docs\plans\citation_system\01_initial_analysis.md
# Index: 4
# Runnable: False
# Hash: 73363f44

# example-metadata:
# runnable: false

def assign_priority(claim: Dict) -> str:
    """
    CRITICAL: Uncited formal theorems/lemmas (scientific credibility risk)
    HIGH: Uncited implementation claims (reproducibility risk)
    MEDIUM: Already cited OR informal claims (lower impact)
    """

    if (claim['category'] == 'theoretical' and
        claim['type'] in ['theorem', 'lemma', 'proposition'] and
        not claim['has_citation']):
        return 'CRITICAL'  # ~29 claims

    if (claim['category'] == 'implementation' and
        claim['type'] == 'implementation' and
        not claim['has_citation']):
        return 'HIGH'  # ~136 claims

    return 'MEDIUM'  # ~335 claims