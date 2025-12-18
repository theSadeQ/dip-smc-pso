"""
data_plotting.py - Data Visualization with Matplotlib

This script demonstrates essential plotting techniques for scientific computing:
- Line plots
- Scatter plots
- Multiple subplots
- Customization (labels, titles, legends, grids)
- Saving figures

Requirements: pip install numpy matplotlib

Run: python data_plotting.py
"""

import numpy as np
import matplotlib.pyplot as plt


def demo_basic_plot():
    """Demonstrate basic line plot."""
    print("\n1. Creating basic line plot...")

    # Generate data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.xlabel("x (radians)")
    plt.ylabel("sin(x)")
    plt.title("Basic Sine Wave")
    plt.grid(True)
    plt.show()


def demo_multiple_lines():
    """Demonstrate multiple lines on same plot."""
    print("\n2. Creating plot with multiple lines...")

    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    plt.plot(x, y3, 'g:', linewidth=2, label='sin(x)*cos(x)')

    plt.xlabel("x (radians)")
    plt.ylabel("y")
    plt.title("Trigonometric Functions")
    plt.legend()
    plt.grid(True)
    plt.show()


def demo_scatter_plot():
    """Demonstrate scatter plot."""
    print("\n3. Creating scatter plot...")

    # Generate random data
    np.random.seed(42)
    x = np.random.randn(100)
    y = 2 * x + 1 + np.random.randn(100) * 0.5

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c='blue', alpha=0.6, edgecolors='k')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatter Plot with Linear Relationship")
    plt.grid(True)

    # Add trend line
    coeffs = np.polyfit(x, y, 1)
    trend_line = np.poly1d(coeffs)
    x_line = np.linspace(x.min(), x.max(), 100)
    plt.plot(x_line, trend_line(x_line), 'r--', linewidth=2, label='Trend line')
    plt.legend()

    plt.show()


def demo_subplots():
    """Demonstrate multiple subplots."""
    print("\n4. Creating multiple subplots...")

    # Generate data
    t = np.linspace(0, 10, 1000)
    signal1 = np.sin(2 * np.pi * t)
    signal2 = np.sin(2 * np.pi * 2 * t)
    signal3 = signal1 + signal2
    signal4 = signal1 * signal2

    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Top-left
    axes[0, 0].plot(t, signal1, 'b-')
    axes[0, 0].set_title("Signal 1: sin(2πt)")
    axes[0, 0].set_xlabel("Time (s)")
    axes[0, 0].set_ylabel("Amplitude")
    axes[0, 0].grid(True)

    # Plot 2: Top-right
    axes[0, 1].plot(t, signal2, 'r-')
    axes[0, 1].set_title("Signal 2: sin(4πt)")
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("Amplitude")
    axes[0, 1].grid(True)

    # Plot 3: Bottom-left
    axes[1, 0].plot(t, signal3, 'g-')
    axes[1, 0].set_title("Sum: Signal 1 + Signal 2")
    axes[1, 0].set_xlabel("Time (s)")
    axes[1, 0].set_ylabel("Amplitude")
    axes[1, 0].grid(True)

    # Plot 4: Bottom-right
    axes[1, 1].plot(t, signal4, 'm-')
    axes[1, 1].set_title("Product: Signal 1 × Signal 2")
    axes[1, 1].set_xlabel("Time (s)")
    axes[1, 1].set_ylabel("Amplitude")
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.show()


def demo_histogram():
    """Demonstrate histogram."""
    print("\n5. Creating histogram...")

    # Generate random data (normal distribution)
    np.random.seed(42)
    data = np.random.randn(1000)

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Normally Distributed Data")
    plt.grid(True, axis='y', alpha=0.3)

    # Add vertical line at mean
    mean = np.mean(data)
    plt.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean = {mean:.2f}')
    plt.legend()

    plt.show()


def demo_bar_chart():
    """Demonstrate bar chart."""
    print("\n6. Creating bar chart...")

    controllers = ['Classical\nSMC', 'STA-SMC', 'Adaptive\nSMC', 'Hybrid\nSTA-SMC']
    settling_time = [2.5, 1.8, 2.2, 1.5]  # seconds

    plt.figure(figsize=(10, 6))
    bars = plt.bar(controllers, settling_time, color=['blue', 'green', 'orange', 'red'], alpha=0.7)
    plt.ylabel("Settling Time (s)")
    plt.title("Controller Performance Comparison")
    plt.grid(True, axis='y', alpha=0.3)

    # Add value labels on bars
    for bar, value in zip(bars, settling_time):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}s',
                ha='center', va='bottom')

    plt.show()


def demo_parametric_plot():
    """Demonstrate parametric plot (phase space)."""
    print("\n7. Creating parametric plot...")

    # Generate data for a spiral
    t = np.linspace(0, 4 * np.pi, 1000)
    r = t / (2 * np.pi)
    x = r * np.cos(t)
    y = r * np.sin(t)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.plot(x[0], y[0], 'go', markersize=12, label='Start')
    plt.plot(x[-1], y[-1], 'ro', markersize=12, label='End')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Parametric Plot: Spiral")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()


def demo_customization():
    """Demonstrate advanced customization."""
    print("\n8. Creating highly customized plot...")

    x = np.linspace(0, 10, 100)
    y1 = np.exp(-0.1 * x) * np.cos(2 * np.pi * x)
    y2 = np.exp(-0.1 * x)
    y3 = -np.exp(-0.1 * x)

    plt.figure(figsize=(12, 8))

    # Main signal
    plt.plot(x, y1, 'b-', linewidth=2, label='Damped oscillation')

    # Envelope
    plt.plot(x, y2, 'r--', linewidth=1.5, label='Upper envelope')
    plt.plot(x, y3, 'r--', linewidth=1.5, label='Lower envelope')

    # Fill between envelopes
    plt.fill_between(x, y2, y3, alpha=0.2, color='red')

    # Customization
    plt.xlabel("Time (s)", fontsize=14, fontweight='bold')
    plt.ylabel("Amplitude", fontsize=14, fontweight='bold')
    plt.title("Damped Harmonic Oscillator", fontsize=16, fontweight='bold')
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)

    # Set axis limits
    plt.xlim([0, 10])
    plt.ylim([-1.2, 1.2])

    # Add annotations
    plt.annotate('Maximum amplitude',
                xy=(0, 1), xytext=(2, 0.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                fontsize=12)

    plt.show()


def demo_save_figure():
    """Demonstrate saving figures to files."""
    print("\n9. Saving figure to file...")

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.xlabel("x (radians)")
    plt.ylabel("sin(x)")
    plt.title("Sine Wave - Saved Figure")
    plt.grid(True)

    # Save to file
    filename = "sine_wave_plot.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   Figure saved as: {filename}")

    plt.close()  # Close without showing


def main():
    """Run all plotting demonstrations."""
    print("=" * 60)
    print("Data Visualization with Matplotlib")
    print("=" * 60)

    demo_basic_plot()
    demo_multiple_lines()
    demo_scatter_plot()
    demo_subplots()
    demo_histogram()
    demo_bar_chart()
    demo_parametric_plot()
    demo_customization()
    demo_save_figure()

    print("\n" + "=" * 60)
    print("All demonstrations complete!")
    print("=" * 60)
    print("\nTip: Close each plot window to proceed to the next plot.")


if __name__ == "__main__":
    main()
