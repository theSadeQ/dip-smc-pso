# Example from: docs\api\simulation_engine_api_reference.md
# Index: 74
# Runnable: True
# Hash: 1666fe89

from src.simulation.results import BatchResultContainer

# Create batch container
batch_result = BatchResultContainer()

# Add multiple trajectories
for i in range(10):
    batch_result.add_trajectory(
        states=x_arr_list[i],
        times=t_arr,
        controls=u_arr_list[i],
        batch_index=i,
        initial_condition=ic_list[i]
    )

# Access specific trajectory
states_3 = batch_result.get_states(batch_index=3)  # (n_steps+1, 6)

# Access all trajectories
all_states = batch_result.get_states()  # (10, n_steps+1, 6)

# Compute aggregate statistics
settling_times = []
for i in range(10):
    states_i = batch_result.get_states(batch_index=i)
    settling_times.append(compute_settling_time(states_i))

mean_settling = np.mean(settling_times)