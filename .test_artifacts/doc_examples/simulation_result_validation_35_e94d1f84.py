# Example from: docs\validation\simulation_result_validation.md
# Index: 35
# Runnable: True
# Hash: e94d1f84

extreme = risk_analysis['extreme_value_analysis']

# 100-year return level
return_100 = extreme['return_levels']['100_year']
print(f"Once-in-100-scenarios worst-case: {return_100:.2f}")