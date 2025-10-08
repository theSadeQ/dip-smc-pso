# Example from: docs\guides\how-to\result-analysis.md
# Index: 5
# Runnable: True
# Hash: 39b7be61

import json
import numpy as np
from scipy import stats

# Load results from two controllers
with open('results_classical.json') as f:
    classical = json.load(f)

with open('results_sta.json') as f:
    sta = json.load(f)

# Extract ISE values
ise_classical = classical['metrics']['ise']
ise_sta = sta['metrics']['ise']

# Compute improvement
improvement = (ise_classical - ise_sta) / ise_classical * 100
print(f"ISE Improvement: {improvement:.1f}%")
print(f"Classical SMC: {ise_classical:.4f}")
print(f"STA-SMC:       {ise_sta:.4f}")