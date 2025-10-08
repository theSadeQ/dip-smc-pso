# Example from: docs\theory\numerical_stability_methods.md
# Index: 5
# Runnable: True
# Hash: ec34fa22

# Issue #13: Standardized division protection
normalized_ranges = [r / (abs(b_min) + abs(b_max) + EPSILON_DIV)
                     for r, b_min, b_max in zip(ranges, bounds_min, bounds_max)]