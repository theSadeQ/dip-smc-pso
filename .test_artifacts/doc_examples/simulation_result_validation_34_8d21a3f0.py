# Example from: docs\validation\simulation_result_validation.md
# Index: 34
# Runnable: True
# Hash: 8d21a3f0

risk_analysis = result.data['risk_analysis']

var_5 = risk_analysis['value_at_risk']['var_5']    # 5th percentile
cvar_5 = risk_analysis['conditional_value_at_risk']['cvar_5']

print(f"Worst 5% scenarios: VaR={var_5:.2f}, CVaR={cvar_5:.2f}")