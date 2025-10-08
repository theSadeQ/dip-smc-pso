# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 8
# Runnable: False
# Hash: f9b2965c

def test_cost_sensitivity():
    """Verify PSO cost function distinguishes good/bad controllers"""
    # Test that different gains produce different costs
    gains_good = [10, 5, 8, 3, 15, 2]
    gains_bad = [100, 100, 100, 100, 100, 100]

    cost_good = evaluate_gains(gains_good)
    cost_bad = evaluate_gains(gains_bad)

    # Good gains should have lower cost
    assert cost_good < cost_bad, "Cost function cannot distinguish controller quality"

    # Costs should not be zero
    assert cost_good > 1e-6, "Good controller cost is suspiciously small"
    assert cost_bad > 1e-3, "Bad controller cost is suspiciously small"