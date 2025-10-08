# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 12
# Runnable: False
# Hash: 19bf2c42

# example-metadata:
# runnable: false

def deduplicate_claims(claims: List[Dict]) -> List[Dict]:
    """
    Remove near-duplicates using Jaccard similarity.

    Strategy:
    1. Generate signature from key terms
    2. Compare pairwise (Jaccard similarity)
    3. Merge if similarity > 0.8
    4. Keep higher-confidence version
    """

    deduplicated = []

    for claim in claims:
        signature = _generate_signature(claim)

        # Check against existing
        is_duplicate = False
        for existing in deduplicated:
            similarity = _calculate_similarity(claim, existing)

            if similarity > 0.8:
                is_duplicate = True
                if claim['confidence'] > existing['confidence']:
                    deduplicated.remove(existing)
                    deduplicated.append(claim)
                break

        if not is_duplicate:
            deduplicated.append(claim)

    return deduplicated

def _generate_signature(claim: Dict) -> str:
    """Extract key technical terms (sorted for consistency)."""
    text = claim.get('claim_text', claim.get('statement', ''))
    terms = [w.lower() for w in text.split() if len(w) > 3]
    return '|'.join(sorted(set(terms[:10])))

def _calculate_similarity(claim1: Dict, claim2: Dict) -> float:
    """Jaccard similarity of key terms."""
    sig1 = set(_generate_signature(claim1).split('|'))
    sig2 = set(_generate_signature(claim2).split('|'))
    intersection = sig1 & sig2
    union = sig1 | sig2
    return len(intersection) / len(union) if union else 0.0