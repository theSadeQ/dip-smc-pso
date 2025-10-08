# Example from: docs\tools\claim_extraction_guide.md
# Index: 5
# Runnable: True
# Hash: 981e8c07

import json

inventory = json.load(open("artifacts/claims_inventory.json"))

# Process CRITICAL claims first
for claim_id in inventory["research_queue"]["CRITICAL"]:
    claim = next(c for c in inventory["claims"] if c["id"] == claim_id)

    # AI research: find ≥2 academic papers
    references = ai_citation_finder(claim["text"], min_refs=2)

    # Validate and store
    validate_references(claim_id, references)