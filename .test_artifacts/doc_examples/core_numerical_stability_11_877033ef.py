# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 11
# Runnable: True
# Hash: 877033ef

stats = monitor.get_statistics()
print(f"Regularization rate: {stats['regularization_rate'] * 100:.1f}%")
print(f"Average condition number: {stats['avg_condition_number']:.2e}")
print(f"Max condition number: {stats['max_condition_number']:.2e}")
print(f"Failure rate: {stats['failed_count'] / stats['total_inversions'] * 100:.2f}%")