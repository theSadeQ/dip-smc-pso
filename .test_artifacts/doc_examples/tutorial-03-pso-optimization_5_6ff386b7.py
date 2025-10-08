# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 5
# Runnable: False
# Hash: 6ff386b7

# example-metadata:
# runnable: false

scenarios = ['small', 'large', 'cart', 'velocity']
results = {}

for scenario in scenarios:
    data = json.load(open(f'test_{scenario}.json'))
    results[scenario] = {
        'ise': data['metrics']['ise'],
        'settling': data['metrics']['settling_time'],
        'stable': data['metrics']['settling_time'] < 10.0  # Stability criterion
    }

# Print summary
print("Robustness Validation:")
for scenario, metrics in results.items():
    status = "✓" if metrics['stable'] else "✗"
    print(f"{status} {scenario:10s}: ISE={metrics['ise']:.3f}, Settling={metrics['settling']:.2f}s")