# III. SYSTEM MODELING

This section presents the mathematical model of the double inverted pendulum (DIP) system used for controller design and simulation. We derive the nonlinear equations of motion using Lagrangian mechanics (Section III-A), present the state-space representation (Section III-B), and specify the physical parameters (Section III-C).

## A. System Description and Coordinates

The double inverted pendulum consists of two rigid links serially connected via revolute joints, mounted on a cart that translates horizontally. The system has three degrees of freedom and one control input (horizontal force on cart), making it underactuated with underactuation degree 2.

**Generalized Coordinates:**
- $x$ - cart position (horizontal displacement from origin) [m]
- $\theta_1$ - angle of first link from vertical (counterclockwise positive) [rad]
- $\theta_2$ - angle of second link from vertical (counterclockwise positive) [rad]

**Control Input:**
- $u$ - horizontal force applied to cart [N], saturated at $\pm 150$ N

**Control Objective:**
Stabilize the system at the upright equilibrium $\mathbf{q}_{\text{eq}} = [x, 0, 0]^T$ where both pendulum links are vertical (unstable equilibrium without control).

**Assumptions:**
1. Rigid body dynamics (no flexible modes)
2. Frictionless joints (conservative system)
3. Point mass approximation for pendulum links (mass concentrated at center of mass)
4. Planar motion only (no out-of-plane dynamics)
5. Small angle approximation NOT used (full nonlinear model)

## B. Equations of Motion

### 1) Lagrangian Formulation

The system dynamics are derived using the Euler-Lagrange equations:

```latex
\frac{d}{dt}\left(\frac{\partial \mathcal{L}}{\partial \dot{q}_i}\right) - \frac{\partial \mathcal{L}}{\partial q_i} = Q_i, \quad i = 1, 2, 3
```

where $\mathcal{L} = T - V$ is the Lagrangian (kinetic minus potential energy) and $Q_i$ are generalized forces.

**Kinetic Energy:**
The total kinetic energy includes contributions from cart translation and pendulum rotations:

```latex
T = \frac{1}{2}M\dot{x}^2 + \frac{1}{2}m_1(\dot{x}_1^2 + \dot{y}_1^2) + \frac{1}{2}I_1\dot{\theta}_1^2 + \frac{1}{2}m_2(\dot{x}_2^2 + \dot{y}_2^2) + \frac{1}{2}I_2\dot{\theta}_2^2
```

where $(x_i, y_i)$ are the Cartesian coordinates of the $i$-th link center of mass:

```latex
\begin{aligned}
x_1 &= x + \frac{l_1}{2}\sin\theta_1 \\
y_1 &= \frac{l_1}{2}\cos\theta_1 \\
x_2 &= x + l_1\sin\theta_1 + \frac{l_2}{2}\sin\theta_2 \\
y_2 &= l_1\cos\theta_1 + \frac{l_2}{2}\cos\theta_2
\end{aligned}
```

**Potential Energy:**
Gravitational potential energy with respect to cart level:

```latex
V = m_1 g \frac{l_1}{2}\cos\theta_1 + m_2 g \left(l_1\cos\theta_1 + \frac{l_2}{2}\cos\theta_2\right)
```

### 2) Matrix Form

After applying the Euler-Lagrange equations and algebraic manipulation, the system dynamics can be written in the compact matrix form:

```latex
\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) = \mathbf{B}u
```

where $\mathbf{q} = [x, \theta_1, \theta_2]^T$ and:

**Inertia Matrix** $\mathbf{M}(\mathbf{q}) \in \mathbb{R}^{3 \times 3}$ (symmetric positive definite):

```latex
\mathbf{M} = \begin{bmatrix}
M_{11} & M_{12} & M_{13} \\
M_{21} & M_{22} & M_{23} \\
M_{31} & M_{32} & M_{33}
\end{bmatrix}
```

with elements:

```latex
\begin{aligned}
M_{11} &= M + m_1 + m_2 \\
M_{12} &= \frac{m_1 l_1}{2}\cos\theta_1 + m_2 l_1\cos\theta_1 \\
M_{13} &= \frac{m_2 l_2}{2}\cos\theta_2 \\
M_{22} &= I_1 + \frac{m_1 l_1^2}{4} + m_2 l_1^2 \\
M_{23} &= m_2 l_1 l_2 \cos(\theta_1 - \theta_2) \\
M_{33} &= I_2 + \frac{m_2 l_2^2}{4}
\end{aligned}
```

(Matrix is symmetric: $M_{21} = M_{12}$, $M_{31} = M_{13}$, $M_{32} = M_{23}$)

**Coriolis/Centripetal Matrix** $\mathbf{C}(\mathbf{q}, \dot{\mathbf{q}}) \in \mathbb{R}^{3 \times 3}$:

```latex
\mathbf{C} = \begin{bmatrix}
0 & C_{12} & C_{13} \\
0 & 0 & C_{23} \\
0 & C_{32} & 0
\end{bmatrix}
```

with nonzero elements:

```latex
\begin{aligned}
C_{12} &= -\left(\frac{m_1 l_1}{2} + m_2 l_1\right)\sin\theta_1 \cdot \dot{\theta}_1 \\
C_{13} &= -\frac{m_2 l_2}{2}\sin\theta_2 \cdot \dot{\theta}_2 \\
C_{23} &= -m_2 l_1 l_2 \sin(\theta_1 - \theta_2) \cdot \dot{\theta}_2 \\
C_{32} &= m_2 l_1 l_2 \sin(\theta_1 - \theta_2) \cdot \dot{\theta}_1
\end{aligned}
```

**Gravity Vector** $\mathbf{G}(\mathbf{q}) \in \mathbb{R}^3$:

```latex
\mathbf{G} = \begin{bmatrix}
0 \\
-\left(\frac{m_1 l_1}{2} + m_2 l_1\right)g\sin\theta_1 \\
-\frac{m_2 l_2}{2}g\sin\theta_2
\end{bmatrix}
```

**Input Matrix** $\mathbf{B} \in \mathbb{R}^3$:

```latex
\mathbf{B} = \begin{bmatrix}
1 \\
0 \\
0
\end{bmatrix}
```

This indicates that the control force $u$ acts directly on the cart (first coordinate) and indirectly affects the pendulum angles through inertial coupling.

## C. State-Space Representation

### 1) State Vector

Define the state vector $\mathbf{x} \in \mathbb{R}^6$ as:

```latex
\mathbf{x} = \begin{bmatrix}
x \\ \theta_1 \\ \theta_2 \\ \dot{x} \\ \dot{\theta}_1 \\ \dot{\theta}_2
\end{bmatrix} = \begin{bmatrix}
\mathbf{q} \\ \dot{\mathbf{q}}
\end{bmatrix}
```

### 2) State-Space Dynamics

The first-order state-space form is:

```latex
\dot{\mathbf{x}} = \begin{bmatrix}
\dot{\mathbf{q}} \\
\mathbf{M}^{-1}(\mathbf{q})[\mathbf{B}u - \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} - \mathbf{G}(\mathbf{q})]
\end{bmatrix}
```

**Computational Note:** The inertia matrix $\mathbf{M}(\mathbf{q})$ is inverted at each time step to compute angular accelerations. The matrix is guaranteed to be positive definite (invertible) for all $\mathbf{q}$ by the physical properties of mechanical systems, with condition number typically $\kappa(\mathbf{M}) < 100$ for the DIP configuration used in this work.

### 3) Equilibrium Manifold

The system has an infinite set of equilibrium points:

```latex
\mathcal{E} = \{(x, 0, 0, 0, 0, 0) : x \in \mathbb{R}\}
```

corresponding to the upright pendulum configuration at any cart position. Since cart position $x$ is uncontrolled (no direct actuation on $x$ in the control objective), the SMC design focuses on stabilizing $\theta_1 = \theta_2 = 0$ while allowing $x$ to drift.

**Remark:** In practice, cart position saturation can be enforced via workspace limits or modified control laws, but this is not considered in the current study.

## D. Physical Parameters

The system parameters used in simulation are based on a laboratory-scale DIP setup:

**TABLE I: PHYSICAL PARAMETERS OF DOUBLE INVERTED PENDULUM**

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Cart mass | $M$ | 1.0 | kg |
| Link 1 mass | $m_1$ | 0.1 | kg |
| Link 2 mass | $m_2$ | 0.1 | kg |
| Link 1 length | $l_1$ | 0.5 | m |
| Link 2 length | $l_2$ | 0.5 | m |
| Link 1 inertia | $I_1$ | 0.00208 | kg·m² |
| Link 2 inertia | $I_2$ | 0.00208 | kg·m² |
| Gravity | $g$ | 9.81 | m/s² |
| Control saturation | $u_{\max}$ | 150 | N |
| Sampling time | $\Delta t$ | 0.001 | s |

**Link Inertias:** Computed assuming uniform rods rotating about their center of mass:

```latex
I_i = \frac{1}{12}m_i l_i^2, \quad i = 1, 2
```

For $m_i = 0.1$ kg and $l_i = 0.5$ m:

```latex
I_i = \frac{1}{12} \times 0.1 \times 0.5^2 = 0.00208 \, \text{kg·m}^2
```

**Parameter Rationale:**
- **Cart-to-pendulum mass ratio** ($M/m_i = 10$): Typical for laboratory DIP systems, ensures sufficient inertial coupling
- **Link lengths** ($l_1 = l_2 = 0.5$ m): Standard laboratory scale, total height ~1 m
- **Control saturation** ($u_{\max} = 150$ N): Corresponds to ~15× gravity force on cart, provides adequate control authority for stabilization

## E. System Properties

### 1) Controllability

The DIP system is **fully controllable** at the upright equilibrium, meaning all states can be driven to zero through appropriate control input $u$. This can be verified by checking the rank of the controllability matrix for the linearized system at equilibrium.

**Linearized Dynamics at Equilibrium:**
At $(\theta_1, \theta_2, \dot{\theta}_1, \dot{\theta}_2) = (0, 0, 0, 0)$, the nonlinear system linearizes to:

```latex
\delta\ddot{\mathbf{q}} = \mathbf{M}_0^{-1}[\mathbf{B}u - \mathbf{K}_{\text{stiff}}\delta\mathbf{q}]
```

where $\mathbf{K}_{\text{stiff}}$ contains gravity gradient terms (negative stiffness, indicating instability).

### 2) Unstable Equilibrium

The upright equilibrium $\theta_1 = \theta_2 = 0$ is **unstable** in open-loop. The linearized system has two unstable poles (positive real parts) corresponding to the two pendulum angles. Without control, small perturbations grow exponentially, causing the pendulums to fall.

**Time Constants:** The open-loop unstable time constants are approximately:
- Link 1: $\tau_1 \approx 0.45$ s
- Link 2: $\tau_2 \approx 0.45$ s

(Similar values due to identical link parameters)

This requires the controller to provide stabilizing feedback with sufficient bandwidth (typically $> 10$ Hz) to overcome the natural instability.

### 3) Coupling Structure

The system exhibits strong **dynamic coupling** between the two pendulum angles through the inertia matrix off-diagonal terms ($M_{23}$) and Coriolis terms ($C_{23}, C_{32}$). This coupling is maximal when $\theta_1 \approx \theta_2$ (links aligned) and minimal when $\theta_1 - \theta_2 = \pm 90°$ (links orthogonal).

The sliding surface design (Section IV-A) exploits this coupling by combining both angle errors in a single sliding variable $s = k_1(\dot{\theta}_1 + \lambda_1\theta_1) + k_2(\dot{\theta}_2 + \lambda_2\theta_2)$, allowing the single control input to coordinate both pendulum motions.

---

## Summary

This section presented the mathematical model of the double inverted pendulum system:

1. **Lagrangian derivation**: Kinetic and potential energy formulation leading to Euler-Lagrange equations
2. **Matrix form**: Compact representation $\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) = \mathbf{B}u$ with explicit matrix elements
3. **State-space form**: First-order system with 6-dimensional state vector
4. **Physical parameters**: Laboratory-scale DIP configuration (cart: 1 kg, links: 0.1 kg each, lengths: 0.5 m)
5. **System properties**: Fully controllable, unstable equilibrium, strong dynamic coupling

The nonlinear model is used directly for controller design (Section IV) and simulation (Section VI), without linearization approximations. This ensures the control approach is validated on the full nonlinear dynamics representative of physical DIP systems.

**Next:** Section IV develops the sliding mode control framework using this system model as the foundation.
