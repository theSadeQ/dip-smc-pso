# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 10
# Runnable: True
# Hash: 55dd791c

def merge_claims():
    formal = json.load(open('artifacts/formal_claims.json'))
    code = json.load(open('artifacts/code_claims.json'))

    all_claims = formal['claims'] + code['claims']