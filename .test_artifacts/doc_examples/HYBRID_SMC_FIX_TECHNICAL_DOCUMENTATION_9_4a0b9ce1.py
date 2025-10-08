# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 9
# Runnable: True
# Hash: 4a0b9ce1

# Test PSO integration directly
factory = create_pso_controller_factory(SMCType.HYBRID, config)
gains = [10, 8, 5, 3]
fitness = factory(gains)
assert isinstance(fitness, float), f"Expected float, got {type(fitness)}"
assert fitness >= 0, f"Invalid fitness: {fitness}"