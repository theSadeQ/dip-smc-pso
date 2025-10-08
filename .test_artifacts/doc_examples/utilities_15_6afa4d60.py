# Example from: docs\guides\api\utilities.md
# Index: 15
# Runnable: True
# Hash: 6afa4d60

from src.utils.analysis import compute_metrics

result = {
    't': t,
    'state': state_trajectory,
    'control': control_sequence
}

metrics = compute_metrics(result)

print(f"ISE: {metrics['ise']:.4f}")
print(f"ITAE: {metrics['itae']:.4f}")
print(f"RMS Control: {metrics['rms_control']:.4f}")
print(f"Settling Time: {metrics['settling_time']:.2f} s")