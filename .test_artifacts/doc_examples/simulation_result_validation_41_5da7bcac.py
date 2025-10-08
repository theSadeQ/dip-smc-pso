# Example from: docs\validation\simulation_result_validation.md
# Index: 41
# Runnable: True
# Hash: 5da7bcac

# Always report effect size
if test['p_value'] < 0.05:
    effect_size = compute_cohens_d(group1, group2)
    if abs(effect_size) < 0.2:
        print("⚠ Statistically significant but negligible effect")