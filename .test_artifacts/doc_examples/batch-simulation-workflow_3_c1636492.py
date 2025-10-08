# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 3
# Runnable: True
# Hash: c1636492

from src.simulation.results.containers import BatchResultContainer

# Assume result_container from orchestrator.execute()

# Access individual trial
trial_0_states = result_container.get_states(batch_index=0)  # (501, 6)
trial_0_times = result_container.get_times(batch_index=0)    # (501,)

# Access all trials
all_states = result_container.get_states()  # (batch_size, 501, 6)
all_times = result_container.get_times()     # (501,) - shared across batch

# Metadata
batch_count = result_container.get_batch_count()  # int