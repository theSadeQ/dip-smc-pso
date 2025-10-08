# Example from: docs\issue_12_pso_implementation_summary.md
# Index: 5
# Runnable: True
# Hash: 33a4b0c9

def test_pso_tuner_chattering_optimization():
       """Verify PSOTuner properly optimizes for chattering."""
       tuner = PSOTuner(controller_factory, config, seed=42)
       result = tuner.optimise(iters_override=10)

       # Assert cost is not zero
       assert result['best_cost'] > 0.0

       # Assert chattering metric is included
       validation = validate_controller_chattering(result['best_pos'])
       assert validation['chattering_index'] < baseline_chattering