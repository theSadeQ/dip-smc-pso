# Example from: docs\guides\user-guide.md
# Index: 3
# Runnable: True
# Hash: 77ce076f

# Load multiple results
results = {
    'classical': json.load(open('results_classical.json')),
    'sta': json.load(open('results_sta.json')),
    'adaptive': json.load(open('results_adaptive.json')),
    'hybrid': json.load(open('results_hybrid.json'))
}

# Create comparison table
import pandas as pd

comparison = []
for name, data in results.items():
    comparison.append({
        'Controller': name,
        'ISE': data['metrics']['ise'],
        'ITAE': data['metrics']['itae'],
        'Settling Time (s)': data['metrics']['settling_time'],
        'Overshoot (%)': data['metrics']['overshoot'],
        'Control Effort': data['metrics']['control_effort']
    })

df = pd.DataFrame(comparison)
df = df.set_index('Controller')

print(df.to_markdown())  # Pretty table output