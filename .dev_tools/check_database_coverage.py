#!/usr/bin/env python3
"""
Check if citation database covers likely Category A claims
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import citation_database as db

# Algorithms from likely Category A claims
algorithms_needed = [
    'rls',
    'recursive least squares',
    'euler',
    'rk4',
    'rk45',
    'pareto',
    'weighted sum',
    'equivalent control',
    'sliding mode',
    'super-twisting',
    'multi-objective optimization'
]

# Concepts from likely Category B claims
concepts_needed = [
    'chattering',
    'robustness'
]

print("CITATION DATABASE COVERAGE CHECK")
print("=" * 80)
print()

print("ALGORITHMS (Category A):")
print("-" * 80)
covered_algo = 0
for algo in algorithms_needed:
    citation = db.find_algorithm_citation(algo)
    if citation:
        print(f"[OK] {algo}: {citation.get('suggested_citation', '')}")
        covered_algo += 1
    else:
        print(f"[MISSING] {algo}")

print()
print(f"Algorithm coverage: {covered_algo}/{len(algorithms_needed)} ({100*covered_algo/len(algorithms_needed):.1f}%)")
print()

print("CONCEPTS (Category B):")
print("-" * 80)
covered_concept = 0
for concept in concepts_needed:
    citation = db.find_concept_citation(concept)
    if citation:
        print(f"[OK] {concept}: {citation.get('suggested_citation', '')}")
        covered_concept += 1
    else:
        print(f"[MISSING] {concept}")

print()
print(f"Concept coverage: {covered_concept}/{len(concepts_needed)} ({100*covered_concept/len(concepts_needed):.1f}%)")
print()

print("OVERALL SUMMARY:")
print("-" * 80)
total_needed = len(algorithms_needed) + len(concepts_needed)
total_covered = covered_algo + covered_concept
print(f"Total citations needed: {total_needed}")
print(f"Covered by database: {total_covered}")
print(f"Missing from database: {total_needed - total_covered}")
print(f"Coverage rate: {100*total_covered/total_needed:.1f}%")
