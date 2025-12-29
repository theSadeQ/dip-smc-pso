#!/usr/bin/env python3
"""Quick test of query diversity improvements."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from query_generator import QueryGenerator

# Test claims from Batch 01
test_claims = [
    {
        "id": "FORMAL-THEOREM-016",
        "text": "If all sliding surface parameters $c_i > 0$, then the sliding surface dynamics are exponentially stable with convergence rates determined by $c_i$.",
    },
    {
        "id": "FORMAL-THEOREM-019",
        "text": "Under the reaching condition {eq}`eq:reaching_condition`, the system reaches the sliding surface in finite time bounded by:",
    },
    {
        "id": "FORMAL-THEOREM-020",
        "text": "The classical SMC law {eq}`eq:classical_smc_structure` with switching gain $\\eta > \\rho$ (where $\\rho$ is the uncertainty bound) ensures global finite-time convergence to the sliding surface.",
    },
    {
        "id": "FORMAL-THEOREM-023",
        "text": "With the boundary layer method, the tracking error is ultimately bounded by:",
    },
]

def main():
    gen = QueryGenerator()

    print("=" * 80)
    print("QUERY DIVERSITY TEST - Final Tuning")
    print("=" * 80)
    print()

    for claim in test_claims:
        print(f"Claim: {claim['id']}")
        print(f"Text: {claim['text'][:70]}...")
        print("-" * 80)

        queries = gen.generate(claim['text'], max_queries=5)
        print(f"Queries Generated: {len(queries)}")
        print()

        for i, query in enumerate(queries, 1):
            print(f"  {i}. [{query.priority}] {query.text}")
            print(f"     Type: {query.query_type}, Keywords: {query.keywords}")

        print()
        print("=" * 80)
        print()

if __name__ == "__main__":
    main()
