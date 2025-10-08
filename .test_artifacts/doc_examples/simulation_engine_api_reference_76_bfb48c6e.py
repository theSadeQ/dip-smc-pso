# Example from: docs\api\simulation_engine_api_reference.md
# Index: 76
# Runnable: True
# Hash: bfb48c6e

result.export('hdf5', 'results/sim_001.h5')

# Load with h5py
import h5py
with h5py.File('results/sim_001.h5', 'r') as f:
    states = f['states'][:]
    times = f['times'][:]
    metadata = dict(f.attrs)