"""
numpy_basics.py - Introduction to NumPy

This script demonstrates essential NumPy operations for scientific computing:
- Creating arrays
- Array operations
- Mathematical functions
- Linear algebra basics

Requirements: pip install numpy

Run: python numpy_basics.py
"""

import numpy as np


def demo_array_creation():
    """Demonstrate different ways to create NumPy arrays."""
    print("\n" + "=" * 60)
    print("ARRAY CREATION")
    print("=" * 60)

    # From lists
    arr1 = np.array([1, 2, 3, 4, 5])
    print(f"From list: {arr1}")

    # Special arrays
    zeros = np.zeros(5)
    print(f"Zeros: {zeros}")

    ones = np.ones((2, 3))
    print(f"Ones (2x3):\n{ones}")

    # Ranges
    arange = np.arange(0, 10, 2)
    print(f"Arange (0, 10, 2): {arange}")

    linspace = np.linspace(0, 1, 5)
    print(f"Linspace (0, 1, 5 points): {linspace}")

    # Random
    np.random.seed(42)  # For reproducibility
    random = np.random.rand(5)
    print(f"Random [0, 1): {random}")


def demo_array_operations():
    """Demonstrate element-wise array operations."""
    print("\n" + "=" * 60)
    print("ARRAY OPERATIONS")
    print("=" * 60)

    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"\na + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"a ** 2 = {a ** 2}")

    # Scalar operations
    print(f"\na + 10 = {a + 10}")
    print(f"a * 2 = {a * 2}")

    # Comparison
    print(f"\na > 3: {a > 3}")
    print(f"Elements > 3: {a[a > 3]}")


def demo_math_functions():
    """Demonstrate mathematical functions."""
    print("\n" + "=" * 60)
    print("MATHEMATICAL FUNCTIONS")
    print("=" * 60)

    # Trigonometry
    angles = np.array([0, np.pi/4, np.pi/2, np.pi])
    print(f"Angles: {angles / np.pi} * π")
    print(f"sin(angles): {np.sin(angles)}")
    print(f"cos(angles): {np.cos(angles)}")

    # Exponentials and logarithms
    x = np.array([1, 2, 3])
    print(f"\nx = {x}")
    print(f"exp(x) = {np.exp(x)}")
    print(f"log(x) = {np.log(x)}")
    print(f"sqrt(x) = {np.sqrt(x)}")


def demo_aggregations():
    """Demonstrate aggregation functions."""
    print("\n" + "=" * 60)
    print("AGGREGATION FUNCTIONS")
    print("=" * 60)

    data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Data: {data}")
    print(f"\nSum: {np.sum(data)}")
    print(f"Mean: {np.mean(data)}")
    print(f"Std dev: {np.std(data):.2f}")
    print(f"Min: {np.min(data)}")
    print(f"Max: {np.max(data)}")

    # 2D arrays
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\nMatrix:\n{matrix}")
    print(f"Sum (all): {np.sum(matrix)}")
    print(f"Sum (columns): {np.sum(matrix, axis=0)}")
    print(f"Sum (rows): {np.sum(matrix, axis=1)}")


def demo_linear_algebra():
    """Demonstrate basic linear algebra operations."""
    print("\n" + "=" * 60)
    print("LINEAR ALGEBRA")
    print("=" * 60)

    # Dot product
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    dot = np.dot(a, b)
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a · b = {dot}")

    # Matrix multiplication
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = A @ B

    print(f"\nA =\n{A}")
    print(f"B =\n{B}")
    print(f"A @ B =\n{C}")

    # Matrix inverse
    A_inv = np.linalg.inv(A)
    print(f"\nA⁻¹ =\n{A_inv}")

    # Verify: A @ A⁻¹ = I
    I = A @ A_inv
    print(f"A @ A⁻¹ (should be identity):\n{I}")

    # Eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"\nEigenvalues of A: {eigenvalues}")


def demo_control_system_application():
    """
    Demonstrate a simple control system calculation.

    State-space model:
        dx/dt = Ax + Bu
    where x is state, u is control input.
    """
    print("\n" + "=" * 60)
    print("CONTROL SYSTEM APPLICATION")
    print("=" * 60)

    # System matrices (simple 2-state system)
    A = np.array([[0, 1], [-2, -3]])
    B = np.array([[0], [1]])

    # Current state: [position, velocity]
    x = np.array([[1.0], [0.5]])

    # Control input (force)
    u = 5.0

    # Calculate state derivative
    x_dot = A @ x + B * u

    print("State-space model: dx/dt = Ax + Bu")
    print(f"\nA (system matrix):\n{A}")
    print(f"\nB (input matrix):\n{B}")
    print(f"\nx (state) [position; velocity]:\n{x}")
    print(f"\nu (control input): {u}")
    print(f"\ndx/dt (state derivative):\n{x_dot}")


def main():
    """Run all demonstrations."""
    print("=" * 60)
    print("NumPy Basics Demonstration")
    print("=" * 60)

    demo_array_creation()
    demo_array_operations()
    demo_math_functions()
    demo_aggregations()
    demo_linear_algebra()
    demo_control_system_application()

    print("\n" + "=" * 60)
    print("Demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
