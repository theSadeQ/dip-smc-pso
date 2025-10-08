# Example from: docs\issue_12_continuation_prompt.md
# Index: 5
# Runnable: True
# Hash: 17ba6bbf

# In optimize_chattering_direct.py, update control extraction logic:
if controller_type == "hybrid_adaptive_sta_smc":
    result = controller.compute_control(state, last_control)
    # Hybrid returns dict, not standard output
    if isinstance(result, dict):
        control_output = result.get('control', result.get('u', 0.0))
    else:
        control_output = float(result)