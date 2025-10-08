# Example from: docs\guides\how-to\result-analysis.md
# Index: 4
# Runnable: True
# Hash: d1804572

# Analyze control effort components
control_array = np.array(control)
peak_control = np.max(np.abs(control_array))
mean_control = np.mean(np.abs(control_array))
rms_control = np.sqrt(np.mean(control_array**2))

print(f"Peak Control: {peak_control:.2f} N")
print(f"Mean Control: {mean_control:.2f} N")
print(f"RMS Control:  {rms_control:.2f} N")