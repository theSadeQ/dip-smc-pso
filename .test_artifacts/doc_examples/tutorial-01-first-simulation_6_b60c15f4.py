# Example from: docs\guides\tutorials\tutorial-01-first-simulation.md
# Index: 6
# Runnable: True
# Hash: b60c15f4

# Compute sliding surface value
s = 5.0*theta1 + 5.0*dtheta1 + 5.0*theta2 + 0.5*dtheta2

# Plot sliding surface over time
plt.plot(t, s)
plt.xlabel('Time (s)')
plt.ylabel('Sliding Surface s')
plt.title('Sliding Surface Evolution')
plt.grid(True)
plt.show()