# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 14
# Runnable: True
# Hash: 818cb5fd

def plot_convergence(self) -> None:
    """Plot PSO convergence history."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Fitness trajectory
    ax1.semilogy(self.fitness_history, 'b-', linewidth=2)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Best Fitness (log scale)')
    ax1.set_title('PSO Convergence')
    ax1.grid(True)

    # Diversity evolution
    ax2.plot(self.diversity_history, 'r-', linewidth=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Swarm Diversity')
    ax2.set_title('Swarm Diversity Evolution')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('pso_convergence.png', dpi=150)
    plt.show()