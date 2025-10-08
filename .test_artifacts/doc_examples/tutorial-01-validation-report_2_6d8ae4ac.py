# Example from: docs\guides\tutorials\tutorial-01-validation-report.md
# Index: 2
# Runnable: True
# Hash: 6d8ae4ac

from scripts.analysis.compute_performance_metrics import compute_all_metrics

# After running simulation (t, x, u arrays)
metrics = compute_all_metrics(t, x, u)

# Display metrics
print(metrics)

# Validate against expected ranges
from scripts.analysis.compute_performance_metrics import validate_against_expected
validation = validate_against_expected(metrics)

if all(validation.values()):
    print("All metrics within expected ranges!")
else:
    print("Some metrics outside expected ranges:")
    for metric, passed in validation.items():
        if not passed:
            print(f"  - {metric}")

# Export to JSON
import json
with open('metrics.json', 'w') as f:
    json.dump(metrics.to_dict(), f, indent=2)