# Citation Tracking: Spong1998 - Underactuated Mechanical Systems

**Full Citation:**
```bibtex
@incollection{Spong1998,
  author = {Mark W. Spong},
  title = {Underactuated Mechanical Systems},
  booktitle = {Control Problems in Robotics and Automation},
  editor = {B. Siciliano and K. P. Valavanis},
  publisher = {Springer-Verlag},
  year = {1998},
  pages = {135--150},
  note = {Lecture Notes in Control and Information Sciences}
}
```

**Document Info:**
- **Pages:** 135-150 (16 pages, PDF pages 1-16)
- **Type:** Book Chapter
- **Author:** Mark W. Spong
- **Institution:** Coordinated Science Laboratory, University of Illinois at Urbana-Champaign, USA
- **File:** `thesis/sources_archive/articles/Spong1998_Underactuated_Mechanical_Systems.pdf`

---

## Document Structure

### Main Sections

1. **Introduction** (pp. 135-136)
2. **Lagrangian Dynamics** (pp. 136-139)
   - Equilibrium Solutions and Controllability
3. **Partial Feedback Linearization** (pp. 140-141)
   - Collocated Linearization
   - Non-collocated Linearization
4. **Cascade Systems** (pp. 141-147)
   - Passivity and Energy Control
   - Lyapunov Functions and Forwarding
   - Hybrid and Switching Control
   - Nonholonomic Systems
5. **Conclusions** (pp. 147-148)
6. **References** (pp. 148-150)

---

## Key Concepts and Definitions

### 1. Underactuated Mechanical Systems

**Definition** (p. 135):
> "Underactuated mechanical systems have fewer control inputs than degrees of freedom and arise in applications, such as space and undersea robots, mobile robots, flexible robots, walking, brachiating, and gymnastic robots."

**LaTeX:**
```latex
\text{Underactuated system: } m < n \text{ (control inputs } m \text{ < degrees of freedom } n\text{)}
```

**Citation:** `\cite[p.~135]{Spong1998}`

---

### 2. Lagrangian Dynamics Formulation

**General Form** (p. 137, Eq. 2.1):

**LaTeX:**
```latex
D(q)\ddot{q} + C(q, \dot{q})\dot{q} + g(q) = B(q)\tau
```

where:
- $q \in \mathbb{R}^n$: generalized coordinates
- $\tau \in \mathbb{R}^m$: input generalized force ($m < n$)
- $B(q) \in \mathbb{R}^{n \times m}$: full rank for all $q$

**Partitioned Form** (pp. 137, Eqs. 2.2-2.3):

**LaTeX:**
```latex
d_{11}\ddot{q}_1 + d_{12}\ddot{q}_2 + h_1(q_1,\dot{q}_1,q_2,\dot{q}_2) + \phi_1(q_1,q_2) = 0 \\
d_{12}\ddot{q}_1 + d_{22}\ddot{q}_2 + h_2(q_1,\dot{q}_1,q_2,\dot{q}_2) + \phi_2(q_1,q_2) = b(q_1,q_2)\tau
```

where $q^T = (q_1^T, q_2^T)$, with $q_1 \in \mathbb{R}^{n-m}$ (passive), $q_2 \in \mathbb{R}^m$ (actuated)

**Citation:** `\cite[Eq.~2.1, p.~137]{Spong1998}`

---

### 3. Example Systems

#### Example 2.1: Two-Link Robot (Acrobot/Pendubot)

**Dynamics** (pp. 137, Eqs. 2.4-2.5):

**LaTeX:**
```latex
d_{11}\ddot{q}_1 + d_{12}\ddot{q}_2 + h_1 + \phi_1 = \tau_1 \\
d_{12}\ddot{q}_1 + d_{22}\ddot{q}_2 + h_2 + \phi_2 = \tau_2
```

**Special Cases:**
- **Acrobot:** $\tau_1 = 0$ (shoulder unactuated)
- **Pendubot:** $\tau_2 = 0$ (elbow unactuated)

**Inertia Terms:**
```latex
d_{11} = m_1\ell_{c1}^2 + m_2(\ell_1^2 + \ell_{c2}^2 + 2\ell_1\ell_{c2}\cos(q_2)) + I_1 + I_2 \\
d_{22} = m_2\ell_{c2}^2 + I_2 \\
d_{12} = m_2(\ell_{c2}^2 + \ell_1\ell_{c2}\cos(q_2)) + I_2
```

**Citation:** `\cite[Example~2.1, p.~137]{Spong1998}`

---

#### Example 2.2: Cart-Pole System

**Dynamics** (p. 137, normalized):

**LaTeX:**
```latex
\ddot{q}_1 + \cos q_1 \ddot{q}_2 - \sin q_1 = 0 \\
\cos q_1 \ddot{q}_1 + 2\ddot{q}_2 - \dot{q}_1^2 \sin q_1 = \tau
```

where $q_1 = \theta$ (pole angle), $q_2 = x$ (cart position), $\tau = F$ (force on cart)

**Citation:** `\cite[Example~2.2, p.~137]{Spong1998}`

---

## Key Theorems and Results

### Definition 3.1: Strong Inertial Coupling (p. 140)

**Statement:**
> "The system (2.2), (2.3) is (locally) Strongly Inertially Coupled if and only if
> $\text{rank}(d_{12}(q)) = n - m$ for all $q \in B$
> where $B$ is a neighborhood of the origin."

**Requirement:** $m \geq n - m$ (number of actuated DOF $\geq$ number of passive DOF)

**Significance:** Allows non-collocated partial feedback linearization

**Citation:** `\cite[Definition~3.1, p.~140]{Spong1998}`

---

### Theorem 4.1: Zero Dynamics as Lagrangian System (p. 142)

**Statement:**
> "Given the Lagrangian mechanical system (2.2), (2.3), the zero dynamics of the collocated feedback equivalent system (3.1), (3.2), equivalently (4.3), also defines a Lagrangian system, in particular, there exists a positive definite scalar (energy) function, $E(\eta)$, such that $L_w E = 0$."

**Significance:** Energy is conserved along zero dynamics manifold

**Citation:** `\cite[Theorem~4.1, p.~142]{Spong1998}`

---

## Control Design Approaches

### 1. Collocated Partial Feedback Linearization (p. 140)

**Linearizes actuated degrees of freedom** $q_2$

**Feedback Equivalent System** (Eqs. 3.1-3.2):

**LaTeX:**
```latex
d_{11}\ddot{q}_1 + h_1 + \phi_1 = -d_{12}u \\
\ddot{q}_2 = u
```

**Control Law:**
```latex
\tau = \alpha(q_1,\dot{q}_1,q_2,\dot{q}_2) + \beta(q_1,q_2)u
```

**Properties:**
- Works for **all** underactuated mechanical systems
- Output $y = q_2$
- Consequence of positive definite inertia matrix

**Citation:** `\cite[Sec.~3.1, p.~140]{Spong1998}`

---

### 2. Non-collocated Partial Feedback Linearization (p. 140-141)

**Linearizes passive degrees of freedom** $q_1$

**Requirements:**
- System must be **Strongly Inertially Coupled**
- Allows control of passive joints through dynamic coupling

**Feedback Equivalent:**
```latex
\ddot{q}_1 = u \\
\ddot{q}_2 = -d_{12}^{\dagger}(d_{11}u + h_1 + \phi_1)
```

where $d_{12}^{\dagger} = d_{12}^T(d_{12}d_{12}^T)^{-1}$ is the pseudo-inverse

**Citation:** `\cite[Sec.~3.2, p.~140]{Spong1998}`

---

### 3. Energy-Based Control (p. 142-143)

**Cascade Form** (Eqs. 4.4-4.5):
```latex
\dot{x} = \tilde{A}x \\
\dot{\eta} = \tilde{w}(\eta, x)
```

where $\tilde{A} = A - BK$ is Hurwitz

**Control Strategy:**
1. Choose $u = -Kx$ to stabilize actuated subsystem
2. Use energy function $E(\eta)$ for zero dynamics
3. Convergence to energy manifold (not fixed point)

**Swingup Control Example:**
- Brings system to neighborhood of equilibrium
- Switch to local stabilizing controller
- Shown for cart-pole (Fig. 4.1, p. 143)

**Citation:** `\cite[Sec.~4.1, pp.~142--143]{Spong1998}`

---

### 4. Forwarding Method (p. 143-144)

**Lyapunov Function Construction:**

**LaTeX:**
```latex
V(\eta, x) = V_0(\eta) + \Phi(\eta, x) + V_1(x)
```

where:
- $V_0(\eta)$: Lyapunov function for zero dynamics
- $V_1(x) = x^TPx$: Lyapunov function for linear subsystem
- $\Phi(\eta, x)$: cross-term satisfying $\dot{\Phi} = -L_{h-gKx}V_0$

**Jurdjevic-Quinn Control:**
```latex
v = -L_GV
```

**Citation:** `\cite[Sec.~4.2, pp.~143--144]{Spong1998}`

---

### 5. Hybrid and Switching Control (p. 145)

**Supervisory Architecture:**
- **Swingup Controller:** Nonlinear, energy-based (global)
- **Balance Controller:** Linear, LQR (local)
- **Supervisor:** Switches based on basin of attraction

**Advantages:**
- Simpler individual controllers
- Handles disturbances by re-swinging
- Mimics biological locomotion patterns

**Example:** Acrobot swingup and balance (Fig. 4.3, p. 146)

**Citation:** `\cite[Sec.~4.3, p.~145]{Spong1998}`

---

## Controllability Properties

### Equilibrium Solutions (p. 139, Eqs. 2.8-2.9)

**For constant input** $\tau = \bar{\tau}$:

**LaTeX:**
```latex
\phi_1(q_1, q_2) = 0 \\
\phi_2(q_1, q_2) = b(q_1, q_2)\bar{\tau}
```

**Cases:**
- **With potential terms:** Isolated fixed points, linearly controllable
- **Without potential terms:** Higher-dimensional equilibria, not linearly controllable

**Nonholonomic Constraints:**
- Equation (2.2) is a dynamic constraint on accelerations
- For Acrobot, Pendubot, PVTOL, TORA: constraints are **completely nonintegrable**
- Consequence: Systems are **(strongly) accessible**

**Citation:** `\cite[Sec.~2.1, p.~139]{Spong1998}`

---

### Brockett's Theorem Application (p. 139)

**Result:** Systems without potential terms **cannot** be stabilized to an equilibrium using time-invariant continuous state feedback

**Implication:** Requires:
- Time-varying control
- Discontinuous control
- Switching/hybrid control

**Citation:** `\cite[p.~139]{Spong1998}`

---

## Figures

### Fig. 2.1 (p. 138): Two-Link Robot
**Description:** Schematic of two-link planar robot
- Link masses $m_1, m_2$
- Link lengths $\ell_1, \ell_2$
- Centers of mass $\ell_{c1}, \ell_{c2}$
- Moments of inertia $I_1, I_2$

**Citation:** `\cite[Fig.~2.1]{Spong1998}`

---

### Fig. 2.2 (p. 138): Cart-Pole System
**Description:** Inverted pendulum on cart
- Cart mass $m_c$
- Pole mass $m_p$
- Pole length $\ell$
- Force $F$ on cart

**Citation:** `\cite[Fig.~2.2]{Spong1998}`

---

### Fig. 4.1 (p. 143): Swingup Control Response
**Description:** Cart-pole swingup using energy-based control
- Pole angle converges to energy manifold
- Cart position shows oscillations then stabilization

**Citation:** `\cite[Fig.~4.1]{Spong1998}`

---

### Fig. 4.2 (p. 146): Supervisory Control Architecture
**Description:** Block diagram showing:
- Swingup Controller
- Balance Controller
- Supervisor (switches between controllers)
- Robot

**Citation:** `\cite[Fig.~4.2]{Spong1998}`

---

### Fig. 4.3 (p. 146): Acrobot Swingup and Balance
**Description:** Time history of successful swingup and balance control

**Citation:** `\cite[Fig.~4.3]{Spong1998}`

---

## Quick Reference Table

| Concept | Key Equation/Property | Page | Citation |
|---------|----------------------|------|----------|
| Underactuated definition | $m < n$ | 135 | `\cite[p.~135]{Spong1998}` |
| Lagrangian dynamics | $D(q)\ddot{q} + C(q,\dot{q})\dot{q} + g(q) = B(q)\tau$ | 137 | `\cite[Eq.~2.1]{Spong1998}` |
| Acrobot | $\tau_1 = 0$ | 137 | `\cite[p.~137]{Spong1998}` |
| Pendubot | $\tau_2 = 0$ | 137 | `\cite[p.~137]{Spong1998}` |
| Collocated linearization | Linearizes $q_2$ (actuated DOF) | 140 | `\cite[Sec.~3.1]{Spong1998}` |
| Strong Inertial Coupling | rank$(d_{12}) = n - m$ | 140 | `\cite[Def.~3.1]{Spong1998}` |
| Zero dynamics energy | $L_w E = 0$ | 142 | `\cite[Theorem~4.1]{Spong1998}` |
| Swingup control | Energy-based to manifold | 143 | `\cite[p.~143]{Spong1998}` |
| Forwarding | $V = V_0 + \Phi + V_1$ | 144 | `\cite[p.~144]{Spong1998}` |

---

## Connection to Thesis Work

### Relevance for DIP-SMC-PSO Project:

1. **Underactuated System Theory:**
   - DIP is underactuated (2 DOF, 1 input)
   - Applies to swing-up problem
   - Partial feedback linearization concepts

2. **Lagrangian Formulation:**
   - Standard form for DIP dynamics
   - Shows structure exploited by SMC

3. **Passivity and Energy:**
   - Energy-based swing-up control
   - Complements SMC stabilization
   - Hybrid control architecture

4. **Zero Dynamics:**
   - Understanding uncontrolled dynamics
   - Critical for stability analysis

### How to Cite for Thesis:

**For Underactuated Systems Background:**
> "Underactuated mechanical systems, having fewer control inputs than degrees of freedom, arise in many applications including gymnastic robots and inverted pendulums \\cite{Spong1998}. The double inverted pendulum considered in this work is an underactuated system with two degrees of freedom but only one control input."

**For Lagrangian Dynamics:**
> "The dynamics of underactuated mechanical systems can be expressed in the Lagrangian form \\cite[Eq.~2.1]{Spong1998}:
> $D(q)\ddot{q} + C(q,\dot{q})\dot{q} + g(q) = B(q)\tau$,
> where the control input matrix $B(q)$ has fewer columns than rows."

**For Partial Feedback Linearization:**
> "Collocated partial feedback linearization \\cite[Sec.~3.1]{Spong1998} is a fundamental property of all underactuated mechanical systems, arising from the positive definiteness of the inertia matrix. This technique linearizes the dynamics of the actuated degrees of freedom."

**For Energy-Based Control:**
> "Energy-based swingup control \\cite[Sec.~4.1]{Spong1998} is effective for bringing underactuated systems from a hanging equilibrium to a neighborhood of the inverted equilibrium, where local stabilization can then be applied."

**For Hybrid Control:**
> "Following the supervisory control architecture proposed by Spong \\cite[Sec.~4.3]{Spong1998}, we implement a hybrid controller that switches between swingup and balance modes based on the system state."

---

## Notes

- **Foundational Paper:** This chapter is a seminal work on underactuated control
- **System Examples:** Acrobot, Pendubot, cart-pole are canonical examples
- **Control Paradigms:** Covers feedback linearization, passivity, forwarding, hybrid control
- **Theoretical Depth:** Includes controllability, accessibility, nonholonomic constraints
- **Practical Focus:** Emphasizes implementable control strategies
- **Missing:** Does not cover SMC specifically (focus is on energy/passivity methods)

**Last Updated:** 2025-12-06
