"""
basic_template.py - Simple Python Project Template

This is a minimal template for starting a Python project.
Copy and modify this file to suit your needs.

Author: [Your Name]
Date: [Date]
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Main entry point for the program.

    Modify this function to implement your project logic.
    """
    print("=" * 60)
    print("PROJECT_NAME")
    print("=" * 60)

    # Example: Generate and plot some data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.title("Example Plot")
    plt.grid(True)
    plt.show()

    print("\nProgram complete!")


if __name__ == "__main__":
    main()
