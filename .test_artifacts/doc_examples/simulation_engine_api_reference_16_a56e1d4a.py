# Example from: docs\api\simulation_engine_api_reference.md
# Index: 16
# Runnable: True
# Hash: a56e1d4a

if not np.all(np.isfinite(x_next)):
       # Truncate and return (NaN or Inf detected)