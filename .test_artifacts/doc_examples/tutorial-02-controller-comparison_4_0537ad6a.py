# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 4
# Runnable: True
# Hash: 0537ad6a

# Track adaptive gain evolution
adapted_gains = data['state_vars']['adaptive_gain']
import matplotlib.pyplot as plt

plt.plot(data['time'], adapted_gains)
plt.xlabel('Time (s)')
plt.ylabel('Adaptive Gain K(t)')
plt.title('Gain Adaptation Trajectory')
plt.grid()
plt.show()