# Example from: docs\workflows\complete_integration_guide.md
# Index: 4
# Runnable: True
# Hash: 975605ae

# Demonstrate hybrid capabilities
from src.controllers.smc.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC

controller = HybridAdaptiveSTASMC(
    gains=[77.6216, 44.449, 17.3134, 14.25],  # PSO-optimized
    dt=0.01,
    max_force=100.0,
    enable_equivalent=True,
    use_relative_surface=False,  # Absolute coordinates
    k1_init=2.0,
    k2_init=1.0,
    gamma1=0.5,
    gamma2=0.3
)

# Monitor hybrid operation
results = run_simulation_with_diagnostics(
    controller=controller,
    duration=10.0,
    diagnostics=['adaptation', 'surface', 'modes']
)

# Generate hybrid analysis report
generate_hybrid_analysis_report(results, 'hybrid_analysis.pdf')