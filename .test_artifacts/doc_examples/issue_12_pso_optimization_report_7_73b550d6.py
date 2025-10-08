# Example from: docs\issue_12_pso_optimization_report.md
# Index: 7
# Runnable: True
# Hash: 73b550d6

def test_pso_tuner_chattering_optimization():
       """Verify PSOTuner properly optimizes for chattering reduction."""
       # Create tuner with chattering-focused cost
       # Run optimization
       # Assert chattering_index decreased
       # Assert cost > 0.0 (no more zero-cost bug)