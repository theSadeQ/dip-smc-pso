# Example from: docs\visualization\PHASE_3_1_COMPLETION_REPORT.md
# Index: 3
# Runnable: True
# Hash: 467d71b5

import pandas as pd
import numpy as np

# DataFrame creation from log data
df = pd.DataFrame(data_rows)

# Sorting and indexing
df = df.sort_values('iteration').reset_index(drop=True)

# Time series calculations
df['elapsed_seconds'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# Rolling statistics
df['improvement'] = df['cost'].shift(1) - df['cost']