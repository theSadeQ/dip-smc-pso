# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 11
# Runnable: False
# Hash: b5c57f72

# Test 1: Direct method call
controller = HybridAdaptiveSTASMC(gains=[77.6, 44.4, 17.3, 14.3])
state = np.array([0.01, 0.05, -0.02, 0.0, 0.0, 0.0])
state_vars = controller.initialize_state()
history = controller.initialize_history()

result = controller.compute_control(state, state_vars, history)

# Validation
assert isinstance(result, HybridSTAOutput)
assert not np.isnan(result.control)
print(f"✅ Control output: {result.control}")
print(f"✅ State vars: {result.state_vars}")
print(f"✅ Sliding surface: {result.sliding_surface}")