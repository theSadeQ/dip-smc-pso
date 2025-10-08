# Example from: docs\tools\claim_extraction_guide.md
# Index: 15
# Runnable: True
# Hash: 0f9689cf

import json
from phase2.ai_researcher import find_citations

# Load Phase 1 output
inventory = json.load(open("artifacts/claims_inventory.json"))

citations = []

# Process CRITICAL queue first (highest priority)
for claim_id in inventory["research_queue"]["CRITICAL"]:
    claim = next(c for c in inventory["claims"] if c["id"] == claim_id)

    # AI research: find ≥2 peer-reviewed papers
    print(f"Researching: {claim['text']}")
    references = find_citations(
        claim_text=claim["text"],
        min_references=2,
        sources=["Google Scholar", "arXiv", "IEEE Xplore"]
    )

    # Validate quality
    validated_refs = [r for r in references if r["relevance_score"] >= 0.8]

    if len(validated_refs) >= 2:
        citations.append({
            "claim_id": claim_id,
            "references": validated_refs,
            "status": "VALIDATED"
        })
    else:
        citations.append({
            "claim_id": claim_id,
            "references": validated_refs,
            "status": "NEEDS_MANUAL_REVIEW"
        })

# Save Phase 2 output
json.dump(citations, open("artifacts/citations_validated.json", "w"), indent=2)