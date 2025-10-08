# Example from: docs\plant\models_guide.md
# Index: 15
# Runnable: True
# Hash: ef91e863

stats = dynamics.get_monitoring_stats()
print(f"Average condition number: {stats['avg_condition_number']:.2e}")
print(f"Regularization rate: {stats['regularization_rate']:.2%}")
print(f"Failure rate: {stats['failure_rate']:.2%}")