# Example from: docs\guides\how-to\result-analysis.md
# Index: 16
# Runnable: True
# Hash: a0a7e1f2

from scipy.io import savemat

# Prepare data for MATLAB
matlab_data = {
    'time': np.array(data['time']),
    'state': np.array(data['state']),
    'control': np.array(data['control']),
    'metrics': {
        'ISE': data['metrics']['ise'],
        'ITAE': data['metrics']['itae'],
        'settling_time': data['metrics']['settling_time']
    }
}

# Save to .mat file
savemat('simulation_results.mat', matlab_data)
print("Exported to simulation_results.mat")