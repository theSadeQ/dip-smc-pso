# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 16
# Runnable: True
# Hash: f6728bc4

def analyze_hybrid_performance(history):
    """Analyze hybrid controller historical performance."""

    import matplotlib.pyplot as plt
    import numpy as np

    # Extract time series
    k1_history = np.array(history['k1'])
    k2_history = np.array(history['k2'])
    s_history = np.array(history['s'])
    u_int_history = np.array(history['u_int'])

    # Create performance plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Adaptive gains evolution
    axes[0,0].plot(k1_history, label='k1')
    axes[0,0].plot(k2_history, label='k2')
    axes[0,0].set_title('Adaptive Gains Evolution')
    axes[0,0].legend()

    # Sliding surface
    axes[0,1].plot(s_history)
    axes[0,1].set_title('Sliding Surface')
    axes[0,1].axhline(y=0, color='r', linestyle='--')

    # Integral term
    axes[1,0].plot(u_int_history)
    axes[1,0].set_title('Integral Control Term')

    # Phase portrait (s vs ṡ)
    s_dot = np.gradient(s_history)
    axes[1,1].plot(s_history, s_dot)
    axes[1,1].set_title('Sliding Surface Phase Portrait')
    axes[1,1].set_xlabel('s')
    axes[1,1].set_ylabel('ṡ')

    plt.tight_layout()
    return fig