# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 4
# Runnable: False
# Hash: 5e242cae

# example-metadata:
# runnable: false

def _calculate_confidence(match, has_cite, has_proof, has_math):
    """
    Calculate extraction confidence [0, 1].

    Boosters (cumulative):
    - Numbered (e.g., "Theorem 1"): +0.2
    - Has citation {cite}: +0.2
    - Has proof block: +0.1
    - Has LaTeX math: +0.1

    Expected distribution:
    - High (0.8-1.0): 60% of formal claims
    - Medium (0.5-0.8): 35%
    - Low (0.0-0.5): 5% (manual review)
    """
    score = 0.5
    if match.group('number'): score += 0.2
    if has_cite: score += 0.2
    if has_proof: score += 0.1
    if has_math: score += 0.1
    return min(max(score, 0.0), 1.0)