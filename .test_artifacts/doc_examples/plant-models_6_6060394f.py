# Example from: docs\guides\api\plant-models.md
# Index: 6
# Runnable: True
# Hash: 6060394f

def analyze_mass_sensitivity():
    """Test controller sensitivity to mass variations."""
    base_params = config.dip_params
    m1_values = np.linspace(0.3, 0.8, 20)
    ise_results = []

    for m1 in m1_values:
        # Create modified parameters
        modified_params = DIPParams(
            m0=base_params.m0,
            m1=m1,  # Vary first pendulum mass
            m2=base_params.m2,
            l1=base_params.l1,
            l2=base_params.l2
        )

        # Run simulation
        dynamics = FullDynamics(modified_params)
        runner = SimulationRunner(config, dynamics_model=dynamics)
        result = runner.run(controller)
        ise_results.append(result['metrics']['ise'])

    return m1_values, ise_results

m1_vals, ise_vals = analyze_mass_sensitivity()

import matplotlib.pyplot as plt
plt.plot(m1_vals, ise_vals)
plt.xlabel('First Pendulum Mass m₁ (kg)')
plt.ylabel('ISE')
plt.title('Controller Sensitivity to Mass Variation')
plt.grid(True)
plt.show()