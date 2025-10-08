# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 25
# Runnable: True
# Hash: b928d3fc

# Limit history storage
max_history_length = 1000  # Keep only recent samples

# Use circular buffers for real-time applications
from collections import deque
history = {
    'k1': deque(maxlen=max_history_length),
    'k2': deque(maxlen=max_history_length),
    's': deque(maxlen=max_history_length),
}