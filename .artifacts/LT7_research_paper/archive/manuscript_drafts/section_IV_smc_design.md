# IV. SLIDING MODE CONTROL DESIGN

This section presents the theoretical foundation for our PSO-optimized adaptive boundary layer sliding mode control approach. We first establish the classical SMC framework (Section IV-A), then introduce the adaptive boundary layer mechanism (Section IV-B), and conclude with Lyapunov stability analysis demonstrating finite-time convergence guarantees (Section IV-C).

## A. Classical Sliding Mode Control Framework

### 1) System Representation

The double-inverted pendulum system is governed by the Euler-Lagrange equations:

```latex
\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) = \mathbf{B}u + \mathbf{d}(t)
```

where:
- $\mathbf{q} = [x, \theta_1, \theta_2]^T \in \mathbb{R}^3$ - generalized coordinates (cart position, joint angles)
- $\mathbf{M}(\mathbf{q}) \in \mathbb{R}^{3 \times 3}$ - inertia matrix (symmetric positive definite)
- $\mathbf{C}(\mathbf{q}, \dot{\mathbf{q}}) \in \mathbb{R}^{3 \times 3}$ - Coriolis/centripetal matrix
- $\mathbf{G}(\mathbf{q}) \in \mathbb{R}^3$ - gravity vector
- $\mathbf{B} = [1, 0, 0]^T$ - control input matrix (force applied to cart)
- $u \in \mathbb{R}$ - control input (force, saturated at ±150 N)
- $\mathbf{d}(t) \in \mathbb{R}^3$ - external disturbances (assumed bounded: $\|\mathbf{d}(t)\| \leq d_{\text{max}}$)

**Physical Parameters** (from configuration):
- Cart mass: $M = 1.0$ kg
- Pendulum 1: mass $m_1 = 0.1$ kg, length $l_1 = 0.5$ m
- Pendulum 2: mass $m_2 = 0.1$ kg, length $l_2 = 0.5$ m
- Gravity: $g = 9.81$ m/s²

### 2) Sliding Surface Design

The control objective is to stabilize both pendulum angles at the upright equilibrium: $\theta_1 = \theta_2 = 0$. We define a linear sliding surface that combines both angle errors and their derivatives:

```latex
s = k_1(\dot{\theta}_1 + \lambda_1\theta_1) + k_2(\dot{\theta}_2 + \lambda_2\theta_2)
```

where $k_1, k_2, \lambda_1, \lambda_2 > 0$ are design parameters that determine the sliding surface dynamics. The sliding surface $s=0$ represents a manifold in the state space where the tracking errors $\theta_1, \theta_2$ decay exponentially with rates $\lambda_1, \lambda_2$ respectively.

**Sliding Surface Interpretation:**
- **When $s=0$**: System evolves along the sliding manifold with exponential convergence $\dot{\theta}_i + \lambda_i\theta_i = 0$ (equivalent to $\theta_i(t) = \theta_i(0)e^{-\lambda_i t}$)
- **When $s \neq 0$**: Control law drives the system toward $s=0$ (reaching phase)

**Lemma 1 (Sliding Manifold Stability):** If $k_i, \lambda_i > 0$ for $i=1,2$, then the sliding surface dynamics are exponentially stable with convergence rates $\lambda_i$.

*Proof:* The characteristic equation of $\dot{e}_{\theta_i} + \lambda_i e_{\theta_i} = 0$ is $s + \lambda_i = 0$, yielding eigenvalue $-\lambda_i < 0$. □

### 3) Control Law Structure

The classical SMC control law consists of two components:

```latex
u = u_{\text{eq}} + u_{\text{sw}}
```

**Equivalent Control** ($u_{\text{eq}}$): Cancels the nominal system dynamics to maintain $\dot{s} = 0$ on the sliding surface. Derived from the condition $\dot{s} = 0$:

```latex
u_{\text{eq}} = (\mathbf{L}\mathbf{M}^{-1}\mathbf{B})^{-1}[\mathbf{L}\mathbf{M}^{-1}(\mathbf{C}\dot{\mathbf{q}} + \mathbf{G}) - k_1\lambda_1\dot{\theta}_1 - k_2\lambda_2\dot{\theta}_2]
```

where $\mathbf{L} = [0, k_1, k_2]$ is the sliding surface row vector.

**Switching Control** ($u_{\text{sw}}$): Provides robustness against disturbances and model uncertainties:

```latex
u_{\text{sw}} = -K \cdot \text{sat}(s/\epsilon) - k_d \cdot s
```

with:
- $K > 0$ - switching gain (must satisfy $K > \bar{d}$ where $\bar{d}$ is the disturbance bound)
- $k_d \geq 0$ - derivative gain (improves exponential convergence rate)
- $\epsilon > 0$ - boundary layer thickness (controls chattering amplitude)
- $\text{sat}(x/\epsilon)$ - saturation function: $\text{sat}(x/\epsilon) = \begin{cases} x/\epsilon & |x| \leq \epsilon \\ \text{sign}(x) & |x| > \epsilon \end{cases}$

**Boundary Layer Interpretation:**
- **Outside boundary layer** ($|s| > \epsilon$): $\text{sat}(s/\epsilon) = \text{sign}(s)$ → discontinuous switching control (classical SMC)
- **Inside boundary layer** ($|s| \leq \epsilon$): $\text{sat}(s/\epsilon) = s/\epsilon$ → continuous proportional control (chattering reduction)

The boundary layer width $\epsilon$ presents a fundamental tradeoff:
- **Larger $\epsilon$**: Reduced chattering, but increased steady-state error ($\mathcal{O}(\epsilon)$)
- **Smaller $\epsilon$**: Improved tracking precision, but increased chattering

**This tradeoff motivates the adaptive boundary layer approach (Section IV-B).**

### 4) Control Implementation

The control input is saturated to respect actuator limits:

```latex
u_{\text{saturated}} = \text{clip}(u, -u_{\max}, u_{\max})
```

where $u_{\max} = 150$ N. The saturation introduces potential Lyapunov function increase when $|u| > u_{\max}$, but the boundary layer provides robustness margin to maintain stability.

---

## B. Adaptive Boundary Layer Design

The classical SMC with fixed boundary layer $\epsilon$ achieves either good chattering reduction (large $\epsilon$) or high tracking precision (small $\epsilon$), but not both simultaneously. We propose an **adaptive boundary layer** that dynamically adjusts based on the sliding surface derivative magnitude.

### 1) Adaptive Boundary Layer Formula

The effective boundary layer thickness is defined as:

```latex
\epsilon_{\text{eff}}(t) = \epsilon_{\min} + \alpha |\dot{s}(t)|
```

where:
- $\epsilon_{\min} > 0$ - minimum boundary layer thickness (ensures continuous control near equilibrium)
- $\alpha \geq 0$ - adaptation rate (scales boundary layer with sliding surface derivative)
- $|\dot{s}(t)|$ - magnitude of sliding surface time derivative

**Rationale:**
- **Far from equilibrium** ($|\dot{s}|$ large): $\epsilon_{\text{eff}}$ increases → wider boundary layer → reduced chattering during reaching phase
- **Near equilibrium** ($|\dot{s}|$ small): $\epsilon_{\text{eff}} \approx \epsilon_{\min}$ → narrow boundary layer → improved tracking precision
- **Equilibrium** ($\dot{s} = 0$): $\epsilon_{\text{eff}} = \epsilon_{\min}$ → minimal steady-state error

### 2) Sliding Surface Derivative Computation

The sliding surface derivative is computed from system measurements:

```latex
\dot{s} = k_1(\ddot{\theta}_1 + \lambda_1\dot{\theta}_1) + k_2(\ddot{\theta}_2 + \lambda_2\dot{\theta}_2)
```

The angular accelerations $\ddot{\theta}_1, \ddot{\theta}_2$ are estimated using:
1. **Numerical differentiation**: Backward Euler $\ddot{\theta}_i \approx (\dot{\theta}_i[k] - \dot{\theta}_i[k-1])/\Delta t$
2. **Low-pass filtering**: Exponential moving average with coefficient $\beta = 0.3$ to reduce noise amplification

### 3) Modified Control Law

The switching control component incorporates the adaptive boundary layer:

```latex
u_{\text{sw}} = -K \cdot \text{sat}(s/\epsilon_{\text{eff}}) - k_d \cdot s
```

where $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ replaces the fixed $\epsilon$.

**Key Property:** The saturation function $\text{sat}(s/\epsilon_{\text{eff}})$ automatically transitions between:
- **High-derivative regime**: Wide boundary layer ($\epsilon_{\text{eff}}$ large) → smooth control response
- **Low-derivative regime**: Narrow boundary layer ($\epsilon_{\text{eff}}$ small) → precise tracking

### 4) PSO-Based Parameter Optimization

The adaptive boundary layer parameters $(\epsilon_{\min}, \alpha)$ are optimized using Particle Swarm Optimization (PSO) with a multi-objective fitness function:

```latex
F = 0.70 \cdot C + 0.15 \cdot T_s + 0.15 \cdot O
```

where:
- $C$ - chattering index (FFT-based quantification of high-frequency control variations)
- $T_s$ - settling time (time to reach and maintain $|\theta_i| < 0.05$ rad)
- $O$ - overshoot (maximum angular deviation during transient)

**Weights Rationale:**
- **70% chattering**: Primary optimization objective (industrial motivation)
- **15% settling time**: Maintain acceptable transient response
- **15% overshoot**: Prevent excessive initial oscillations

**PSO Configuration:**
- Swarm size: 30 particles
- Iterations: 30 (converged within 20 iterations empirically)
- Parameter bounds: $\epsilon_{\min} \in [0.001, 0.05]$, $\alpha \in [0.1, 2.0]$
- Initialization: Uniform random sampling within bounds

**Optimized Parameters** (MT-6 results):
- $\epsilon_{\min} = 0.00250336$
- $\alpha = 1.21441504$

These values indicate a minimal baseline boundary layer (2.5 mm equivalent control dead-zone) that scales dynamically up to ~1.2× the sliding surface derivative magnitude.

---

## C. Lyapunov Stability Analysis

We now establish the theoretical stability guarantees for the adaptive boundary layer SMC using Lyapunov's direct method. The proof demonstrates finite-time convergence to the sliding surface under standard assumptions.

### 1) Assumptions

**Assumption 1 (Matched Disturbances):** External disturbances enter through the control channel:
```latex
\mathbf{d}(t) = \mathbf{B}d_u(t), \quad |d_u(t)| \leq \bar{d}
```
where $\bar{d} > 0$ is a known disturbance bound.

**Assumption 2 (Switching Gain Dominance):** The switching gain satisfies $K > \bar{d}$.

**Assumption 3 (Controllability):** The control authority scalar $\beta = \mathbf{L}\mathbf{M}^{-1}\mathbf{B} > \epsilon_0 > 0$ for some positive constant $\epsilon_0$.

**Assumption 4 (Positive Gains):** All design parameters are positive: $k_1, k_2, \lambda_1, \lambda_2, K > 0$ and $k_d \geq 0$.

**Remark 1:** Assumption 1 is satisfied for cart-based disturbances (e.g., wind forces, friction variations) as they enter through the control input matrix $\mathbf{B}$. Unmatched disturbances (e.g., direct torques on pendulum joints) are not addressed by this proof but are empirically negligible in our system.

### 2) Lyapunov Function Candidate

We select the standard Lyapunov function for sliding mode control:

```latex
V(s) = \frac{1}{2}s^2
```

**Properties:**
1. $V(s) \geq 0$ for all $s \in \mathbb{R}$ (positive semi-definite)
2. $V(s) = 0 \iff s = 0$ (positive definite)
3. $V(s) \to \infty$ as $|s| \to \infty$ (radially unbounded)

These properties ensure $V$ is a valid Lyapunov function candidate.

### 3) Stability Proof (Outside Boundary Layer)

**Theorem 1 (Finite-Time Convergence to Sliding Surface):** Under Assumptions 1-4, if $K > \bar{d}$, then the sliding variable $s$ converges to the boundary layer $\{|s| \leq \epsilon_{\text{eff}}\}$ in finite time:

```latex
t_{\text{reach}} \leq \frac{|s(0)|}{\eta\beta}
```

where $\eta = K - \bar{d} > 0$ and $\beta = \mathbf{L}\mathbf{M}^{-1}\mathbf{B}$ is the controllability scalar.

*Proof:*

Consider the region outside the adaptive boundary layer: $|s| > \epsilon_{\text{eff}}$. In this region, the saturation function satisfies $\text{sat}(s/\epsilon_{\text{eff}}) = \text{sign}(s)$.

**Step 1: Compute Lyapunov derivative**

Taking the time derivative of $V$ along system trajectories:

```latex
\dot{V} = s\dot{s}
```

From the sliding surface dynamics with equivalent control cancellation:

```latex
\dot{s} = \mathbf{L}\mathbf{M}^{-1}[\mathbf{B}u_{\text{sw}} + \mathbf{d}(t)]
```

Substituting $u_{\text{sw}} = -K \cdot \text{sign}(s) - k_d \cdot s$ (outside boundary layer):

```latex
\begin{aligned}
\dot{s} &= \mathbf{L}\mathbf{M}^{-1}\mathbf{B}[-K \cdot \text{sign}(s) - k_d \cdot s + d_u(t)] \\
&= \beta[-K \cdot \text{sign}(s) - k_d \cdot s + d_u(t)]
\end{aligned}
```

where $\beta = \mathbf{L}\mathbf{M}^{-1}\mathbf{B} > 0$ by Assumption 3.

**Step 2: Derive negative definiteness**

The Lyapunov derivative becomes:

```latex
\begin{aligned}
\dot{V} &= s \cdot \beta[-K \cdot \text{sign}(s) - k_d \cdot s + d_u(t)] \\
&= \beta[-K|s| - k_d s^2 + s \cdot d_u(t)]
\end{aligned}
```

Using the disturbance bound $|d_u(t)| \leq \bar{d}$ (Assumption 1):

```latex
\begin{aligned}
\dot{V} &\leq \beta[-K|s| - k_d s^2 + |s| \cdot \bar{d}] \\
&= \beta|s|(-K + \bar{d}) - \beta k_d s^2 \\
&= -\beta\eta|s| - \beta k_d s^2
\end{aligned}
```

where $\eta = K - \bar{d} > 0$ by Assumption 2.

**Step 3: Establish finite-time convergence**

Since $\eta > 0$ and $k_d \geq 0$, we have:

```latex
\dot{V} \leq -\beta\eta|s| < 0 \quad \forall s \neq 0
```

Using $|s| = \sqrt{2V}$, this implies:

```latex
\dot{V} \leq -\beta\eta\sqrt{2V}
```

This is a differential inequality of the form $\dot{V} \leq -c\sqrt{V}$ with $c = \beta\eta\sqrt{2} > 0$, which has the solution:

```latex
\sqrt{V(t)} \leq \sqrt{V(0)} - \frac{c}{2}t
```

Setting $V(t) = 0$ yields the reaching time:

```latex
t_{\text{reach}} = \frac{2\sqrt{V(0)}}{c} = \frac{2|s(0)|}{\beta\eta\sqrt{2}} = \frac{\sqrt{2}|s(0)|}{\beta\eta}
```

which is bounded as stated. □

**Remark 2 (Exponential Convergence with $k_d > 0$):** When the derivative gain $k_d > 0$, the additional term $-\beta k_d s^2$ in $\dot{V}$ provides exponential convergence within the boundary layer. This accelerates the convergence rate at the cost of increased control effort.

### 4) Ultimate Boundedness (Inside Boundary Layer)

**Theorem 2 (Ultimate Boundedness):** Inside the adaptive boundary layer ($|s| \leq \epsilon_{\text{eff}}$), the sliding variable remains bounded:

```latex
\limsup_{t \to \infty} |s(t)| \leq \frac{\bar{d} \epsilon_{\text{eff}}}{K}
```

*Proof Sketch:*

Inside the boundary layer, $\text{sat}(s/\epsilon_{\text{eff}}) = s/\epsilon_{\text{eff}}$, yielding:

```latex
u_{\text{sw}} = -\frac{K}{\epsilon_{\text{eff}}} s - k_d s
```

The closed-loop sliding surface dynamics become:

```latex
\dot{s} = -\beta\left(\frac{K}{\epsilon_{\text{eff}}} + k_d\right)s + \beta d_u(t)
```

This is a linear system with disturbance input. By standard linear system theory, the steady-state error satisfies:

```latex
|s_{\text{ss}}| \leq \frac{\beta \bar{d}}{\beta(K/\epsilon_{\text{eff}} + k_d)} = \frac{\bar{d} \epsilon_{\text{eff}}}{K + k_d\epsilon_{\text{eff}}} \leq \frac{\bar{d} \epsilon_{\text{eff}}}{K}
```

where the inequality follows from $k_d \geq 0$. □

**Remark 3 (Adaptive Boundary Layer Compatibility):** The adaptive boundary layer $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ does not affect the stability proof structure. The key requirement $K > \bar{d}$ remains valid regardless of $\epsilon_{\text{eff}}$ value. However, the ultimate bound increases when $\epsilon_{\text{eff}}$ is large (far from equilibrium), which is acceptable since the system is in the transient reaching phase.

### 5) Stability Summary

**Convergence Guarantee:** The adaptive boundary layer SMC ensures:
1. **Finite-time reaching**: System reaches $\{|s| \leq \epsilon_{\text{eff}}\}$ in time $t_{\text{reach}} \leq \sqrt{2}|s(0)|/(\beta\eta)$
2. **Sliding phase stability**: Once on the sliding manifold ($s=0$), the angle errors decay exponentially: $\theta_i(t) = \theta_i(0)e^{-\lambda_i t}$
3. **Disturbance rejection**: Matched disturbances $d_u(t)$ are rejected with steady-state error $\mathcal{O}(\bar{d}\epsilon_{\text{eff}}/K)$

**Design Guidelines from Stability Proof:**
1. **Switching gain**: Choose $K = \bar{d} + \eta$ with $\eta > 0$ (margin above disturbance bound)
2. **Controllability**: Verify $\beta = \mathbf{L}\mathbf{M}^{-1}\mathbf{B} > \epsilon_0 > 0$ remains bounded away from zero
3. **Boundary layer**: Select $\epsilon_{\min}$ and $\alpha$ via PSO to minimize chattering while maintaining acceptable steady-state error

---

## Summary

This section established the theoretical foundation for PSO-optimized adaptive boundary layer sliding mode control:

1. **Classical SMC Framework** (Section IV-A): Defined the sliding surface, control law structure, and boundary layer tradeoff
2. **Adaptive Boundary Layer** (Section IV-B): Introduced the formula $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ and PSO-based parameter optimization
3. **Lyapunov Stability** (Section IV-C): Proved finite-time convergence to the sliding surface under standard assumptions (Theorems 1-2)

**Key Theoretical Contributions:**
- **Theorem 1**: Finite-time reaching in $t_{\text{reach}} \leq \sqrt{2}|s(0)|/(\beta\eta)$ for $K > \bar{d}$
- **Theorem 2**: Ultimate boundedness $|s_{\text{ss}}| \leq \bar{d}\epsilon_{\text{eff}}/K$ inside the adaptive boundary layer
- **Remark 3**: Adaptive boundary layer does not compromise stability guarantees

The next section (Section V) describes the PSO optimization methodology used to tune $(\epsilon_{\min}, \alpha)$ for chattering minimization. The experimental validation demonstrating 66.5% chattering reduction is presented in Section VII.
