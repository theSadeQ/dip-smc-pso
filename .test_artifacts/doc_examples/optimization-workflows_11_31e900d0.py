# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 11
# Runnable: True
# Hash: 31e900d0

# Test cost function manually
test_gains = [10, 8, 15, 12, 50, 5]
result = evaluate_controller(test_gains)
cost = compute_cost(result['metrics'], config)
print(f"Test cost: {cost:.4f}")

# Try different gains, ensure cost changes