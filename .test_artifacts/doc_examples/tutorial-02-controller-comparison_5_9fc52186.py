# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 5
# Runnable: False
# Hash: 9fc52186

boundary_layers = [0.001, 0.01, 0.1]
chattering_indices = []

for bl in boundary_layers:
    data = json.load(open(f'bl_{bl}.json'))
    u = np.array(data['control'])
    chattering = compute_chattering_index(u, dt=0.01)
    chattering_indices.append(chattering)

# Plot results
plt.plot(boundary_layers, chattering_indices, 'o-', label='Classical SMC')
plt.axhline(sta_chattering, color='red', linestyle='--', label='STA-SMC')
plt.xlabel('Boundary Layer ε')
plt.ylabel('Chattering Index (N/s)')
plt.xscale('log')
plt.legend()
plt.grid()
plt.show()