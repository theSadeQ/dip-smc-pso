# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 7
# Runnable: True
# Hash: 5434c04f

# Check if adaptation is occurring
data = json.load(open('results_adaptive.json'))
gain_trajectory = data['state_vars']['adaptive_gain']

if np.std(gain_trajectory) < 0.1:
    print("WARNING: Adaptation not occurring")
    print(f"Final gain: {gain_trajectory[-1]:.2f}")
    print(f"Initial gain: {gain_trajectory[0]:.2f}")