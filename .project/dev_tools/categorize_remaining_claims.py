#!/usr/bin/env python3
"""
Categorize remaining 91 claims to determine which need citations
"""
import json
from pathlib import Path
from collections import Counter

# Keywords that indicate algorithmic implementation (likely Category A)
ALGORITHM_KEYWORDS = [
    'rls', 'recursive least squares', 'kalman', 'particle swarm', 'pso',
    'gradient descent', 'optimization', 'runge-kutta', 'rk4', 'euler',
    'adaptive estimation', 'parameter estimation', 'observer',
    'switching logic', 'lyapunov', 'stability', 'convergence',
    'super-twisting', 'sliding mode', 'equivalent control',
    'newton', 'bfgs', 'nelder-mead', 'powell', 'differential evolution',
    'genetic algorithm', 'simulated annealing', 'monte carlo'
]

# Keywords that indicate theoretical concepts (likely Category B)
CONCEPT_KEYWORDS = [
    'chattering', 'overshoot', 'settling time', 'rise time',
    'steady-state error', 'robustness', 'stability margin',
    'nyquist', 'bode', 'root locus', 'controllability',
    'observability', 'reachability', 'lqr', 'mpc theory'
]

# Keywords that indicate pure implementation (Category C)
IMPLEMENTATION_KEYWORDS = [
    'initialize', 'reset', 'cleanup', 'get', 'set',
    'property', 'getter', 'setter', 'factory', 'create',
    'validate', 'check', 'parse', 'format', 'convert',
    'helper', 'utility', 'wrapper', 'interface', 'abstract'
]

def categorize_claim(claim):
    """Categorize a single claim based on context and description"""
    context = claim.get('context', '').lower()
    description = claim.get('description', '').lower()
    combined = context + ' ' + description

    # Check for algorithms
    for keyword in ALGORITHM_KEYWORDS:
        if keyword in combined:
            return 'likely_A', keyword

    # Check for concepts
    for keyword in CONCEPT_KEYWORDS:
        if keyword in combined:
            return 'likely_B', keyword

    # Check for pure implementation
    for keyword in IMPLEMENTATION_KEYWORDS:
        if keyword in combined:
            return 'likely_C', keyword

    # Check file path patterns
    file_path = claim.get('file_path', '').lower()
    if 'interface' in file_path or 'factory' in file_path:
        return 'likely_C', 'interface/factory file'

    # Default: needs manual review
    return 'needs_review', 'no clear pattern'

# Load remaining claims
remaining_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/remaining_91_claims.json')
with open(remaining_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    remaining = data['full_claims']

print(f"CATEGORIZATION OF REMAINING 91 CLAIMS")
print(f"=" * 80)

# Categorize all claims
categorized = {
    'likely_A': [],
    'likely_B': [],
    'likely_C': [],
    'needs_review': []
}

for claim in remaining:
    category, reason = categorize_claim(claim)
    categorized[category].append({
        'claim': claim,
        'reason': reason
    })

# Print summary
print(f"\nSummary:")
print(f"  Likely Category A (algorithm papers): {len(categorized['likely_A'])}")
print(f"  Likely Category B (concept textbooks): {len(categorized['likely_B'])}")
print(f"  Likely Category C (no citation): {len(categorized['likely_C'])}")
print(f"  Needs manual review: {len(categorized['needs_review'])}")
print()

# Show likely Category A claims (need algorithm citations)
if categorized['likely_A']:
    print(f"LIKELY CATEGORY A - Algorithm Implementations ({len(categorized['likely_A'])} claims):")
    print("-" * 80)
    for item in categorized['likely_A']:
        c = item['claim']
        desc = c.get('description', '').encode('ascii', 'replace').decode('ascii')[:60]
        context = c.get('context', '').encode('ascii', 'replace').decode('ascii')[:60]
        print(f"  {c['id']}: {desc}")
        print(f"    Context: {context}...")
        print(f"    Keyword: {item['reason']}")
        print(f"    File: {c.get('file_path', '')}")
        print()

# Show likely Category B claims (need concept citations)
if categorized['likely_B']:
    print(f"\nLIKELY CATEGORY B - Theoretical Concepts ({len(categorized['likely_B'])} claims):")
    print("-" * 80)
    for item in categorized['likely_B']:
        c = item['claim']
        desc = c.get('description', '').encode('ascii', 'replace').decode('ascii')[:60]
        context = c.get('context', '').encode('ascii', 'replace').decode('ascii')[:60]
        print(f"  {c['id']}: {desc}")
        print(f"    Context: {context}...")
        print(f"    Keyword: {item['reason']}")
        print()

# Show needs review sample
if categorized['needs_review']:
    print(f"\nNEEDS MANUAL REVIEW ({len(categorized['needs_review'])} claims) - Sample:")
    print("-" * 80)
    for item in categorized['needs_review'][:10]:
        c = item['claim']
        desc = c.get('description', '').encode('ascii', 'replace').decode('ascii')[:60]
        context = c.get('context', '').encode('ascii', 'replace').decode('ascii')[:80]
        print(f"  {c['id']}: {desc}")
        print(f"    Context: {context}...")
        print()

# Save categorized results
output_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/remaining_91_categorized.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        'summary': {
            'likely_A': len(categorized['likely_A']),
            'likely_B': len(categorized['likely_B']),
            'likely_C': len(categorized['likely_C']),
            'needs_review': len(categorized['needs_review'])
        },
        'categorized': {
            'likely_A': [{'id': item['claim']['id'], 'reason': item['reason']} for item in categorized['likely_A']],
            'likely_B': [{'id': item['claim']['id'], 'reason': item['reason']} for item in categorized['likely_B']],
            'likely_C': [{'id': item['claim']['id'], 'reason': item['reason']} for item in categorized['likely_C']],
            'needs_review': [{'id': item['claim']['id'], 'reason': item['reason']} for item in categorized['needs_review']]
        }
    }, f, indent=2)

print(f"\nSaved categorization to: {output_path}")
