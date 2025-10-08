# Example from: docs\api\simulation_engine_api_reference.md
# Index: 68
# Runnable: True
# Hash: bc4a7559

from src.simulation.results import StandardResultContainer

# Create container
result = StandardResultContainer()

# Add simulation data
result.add_trajectory(
    states=x_arr,
    times=t_arr,
    controls=u_arr,
    controller_type='classical_smc',
    initial_state=x0
)

# Access data
states = result.get_states()  # (n_steps+1, 6)
times = result.get_times()    # (n_steps+1,)

# Export
result.export('csv', 'results/simulation_001.csv')
result.export('hdf5', 'results/simulation_001.h5')