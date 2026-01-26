# E003: Plant Models and Dynamics

## Introduction

Plant models are the mathematical representations of the physical system we want to control. For the double-inverted pendulum (DIP), we need equations that describe how the system moves in response to applied forces.

This episode covers:
- Lagrangian mechanics derivation
- Three model variants (simplified, full, low-rank)
- Model accuracy and computational trade-offs
- Singularities and numerical challenges
- Implementation in Python

## Physical System Description

### Double-Inverted Pendulum Configuration

```
        ●  mass m₂, length L₂
        |
        |  ← Pendulum 2
        |
        ●  mass m₁, length L₁
        |
        |  ← Pendulum 1
        |
    ===========  mass M, position x
        ↕ F
    -----------
     Track/Rail
```

**System Parameters:**
- Cart: mass `M`, position `x`, friction `b_c`
- Pendulum 1: mass `m₁`, length `L₁`, COM `l_c1`, inertia `I₁`, joint friction `b_1`
- Pendulum 2: mass `m₂`, length `L₂`, COM `l_c2`, inertia `I₂`, joint friction `b_2`
- Gravity: `g = 9.81 m/s²`

**Generalized Coordinates:**
```
q = [x, θ₁, θ₂]ᵀ

Where:
  x = cart position [m]
  θ₁ = angle of pendulum 1 from vertical [rad] (0 = upright)
  θ₂ = angle of pendulum 2 from vertical [rad] (0 = upright)
```

**Default Values** (from `config.yaml`):
```yaml
physics:
  cart_mass: 1.5          # kg
  pendulum1_mass: 0.2     # kg
  pendulum2_mass: 0.15    # kg
  pendulum1_length: 0.4   # m
  pendulum2_length: 0.3   # m
  pendulum1_com: 0.2      # m (center of mass from pivot)
  pendulum2_com: 0.15     # m
  pendulum1_inertia: 0.0081  # kg·m²
  pendulum2_inertia: 0.0034  # kg·m²
  gravity: 9.81           # m/s²
  cart_friction: 0.2      # N·s/m
  joint1_friction: 0.005  # N·m·s/rad
  joint2_friction: 0.004  # N·m·s/rad
```

## Lagrangian Mechanics Derivation

### Why Lagrangian Approach?

**Advantages over Newtonian mechanics:**
1. No need to solve for constraint forces
2. Systematic procedure (works for any mechanism)
3. Coordinate-free formulation
4. Easy to add/remove components

**Lagrangian Method Steps:**
1. Choose generalized coordinates `q`
2. Compute kinetic energy `T(q, q̇)`
3. Compute potential energy `V(q)`
4. Form Lagrangian: `L = T - V`
5. Apply Euler-Lagrange equations

### Step 1: Kinetic Energy

**Cart Kinetic Energy:**
```
T_cart = (1/2)M·ẋ²
```

**Pendulum 1 Kinetic Energy:**

Position of COM:
```
x_c1 = x + l_c1·sin(θ₁)
y_c1 = l_c1·cos(θ₁)
```

Velocity:
```
ẋ_c1 = ẋ + l_c1·cos(θ₁)·θ̇₁
ẏ_c1 = -l_c1·sin(θ₁)·θ̇₁
```

Kinetic energy (translation + rotation):
```
T₁ = (1/2)m₁·(ẋ_c1² + ẏ_c1²) + (1/2)I₁·θ̇₁²
   = (1/2)m₁·[ẋ² + 2ẋ·l_c1·cos(θ₁)·θ̇₁ + l_c1²·θ̇₁²] + (1/2)I₁·θ̇₁²
```

**Pendulum 2 Kinetic Energy:**

Position of COM (relative to pendulum 1 pivot):
```
x_c2 = x + L₁·sin(θ₁) + l_c2·sin(θ₂)
y_c2 = L₁·cos(θ₁) + l_c2·cos(θ₂)
```

Velocity:
```
ẋ_c2 = ẋ + L₁·cos(θ₁)·θ̇₁ + l_c2·cos(θ₂)·θ̇₂
ẏ_c2 = -L₁·sin(θ₁)·θ̇₁ - l_c2·sin(θ₂)·θ̇₂
```

Kinetic energy:
```
T₂ = (1/2)m₂·(ẋ_c2² + ẏ_c2²) + (1/2)I₂·θ̇₂²
```

**Total Kinetic Energy:**
```
T = T_cart + T₁ + T₂
```

### Step 2: Potential Energy

```
V = m₁·g·l_c1·cos(θ₁) + m₂·g·(L₁·cos(θ₁) + l_c2·cos(θ₂))
```

(Zero reference at θ₁ = θ₂ = π/2, i.e., horizontal)

### Step 3: Euler-Lagrange Equations

```
d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = Qᵢ

Where Qᵢ = generalized force (includes friction + control input)
```

**For our system:**
```
Q = [F - b_c·ẋ,  -b₁·θ̇₁,  -b₂·θ̇₂]ᵀ

Where F = control force applied to cart
```

### Step 4: Equation of Motion Form

After lengthy algebra, we get:

```
M(q)·q̈ + C(q,q̇)·q̇ + G(q) = Bu + d

Where:
  M(q) = mass/inertia matrix (3×3, symmetric, positive definite)
  C(q,q̇) = Coriolis/centrifugal matrix (3×3)
  G(q) = gravity vector (3×1)
  B = input distribution matrix (3×1, constant)
  u = control input (scalar)
  d = disturbances (friction, external forces)
```

## Mass Matrix Structure

### Full Nonlinear Mass Matrix

```python
def _compute_mass_matrix(self, theta1: float, theta2: float) -> np.ndarray:
    """
    Compute M(q) for full nonlinear model.

    M = [M₁₁  M₁₂  M₁₃]
        [M₂₁  M₂₂  M₂₃]
        [M₃₁  M₃₂  M₃₃]

    Symmetric: M₁₂=M₂₁, M₁₃=M₃₁, M₂₃=M₃₂
    """
    c1 = np.cos(theta1)
    c2 = np.cos(theta2)
    c12 = np.cos(theta1 - theta2)

    # Diagonal elements
    M11 = self.M + self.m1 + self.m2
    M22 = self.I1 + self.m1 * self.lc1**2 + self.m2 * self.L1**2
    M33 = self.I2 + self.m2 * self.lc2**2

    # Off-diagonal elements (coupling terms)
    M12 = (self.m1 * self.lc1 + self.m2 * self.L1) * c1
    M13 = self.m2 * self.lc2 * c2
    M23 = self.m2 * self.L1 * self.lc2 * c12

    return np.array([
        [M11, M12, M13],
        [M12, M22, M23],
        [M13, M23, M33]
    ])
```

**Key Properties:**
1. **Symmetric**: `M = Mᵀ` (always true for Lagrangian systems)
2. **Positive Definite**: All eigenvalues > 0 (kinetic energy always positive)
3. **Configuration-Dependent**: Changes with `θ₁, θ₂`
4. **Bounded**: `λ_min(M) ≥ m_min > 0` (invertible)

### Singularities and Conditioning

**Condition Number:**
```
κ(M) = λ_max(M) / λ_min(M)
```

**Interpretation:**
- `κ ≈ 1`: Well-conditioned (easy to invert)
- `κ > 10⁶`: Ill-conditioned (numerical errors amplified)
- `κ → ∞`: Singular (non-invertible)

**For DIP:**
- Typical: `κ(M) ~ 10-100` (well-conditioned)
- Near horizontal (`θ₁,θ₂ ≈ π/2`): `κ(M) ~ 10⁴-10⁶` (ill-conditioned)
- At singularity: `κ(M) → ∞` (rare, requires exact alignment)

**Code Implementation:**

```python
# Compute condition number
cond = np.linalg.cond(M)

if cond > self.singularity_threshold:  # Default: 1e8
    # Use pseudoinverse with regularization
    M_inv = np.linalg.pinv(M, rcond=1e-6)
else:
    # Standard inversion (faster)
    M_inv = np.linalg.inv(M)
```

From `config.yaml`:
```yaml
physics:
  singularity_cond_threshold: 100000000.0  # 1e8
```

## Coriolis and Centrifugal Terms

### Coriolis/Centrifugal Matrix

```python
def _compute_coriolis_matrix(self, theta1: float, theta2: float,
                            theta1_dot: float, theta2_dot: float) -> np.ndarray:
    """
    Compute C(q,q̇) matrix.

    Contains:
    - Coriolis terms (velocity-dependent coupling)
    - Centrifugal terms (velocity-squared terms)
    """
    s1 = np.sin(theta1)
    s2 = np.sin(theta2)
    s12 = np.sin(theta1 - theta2)

    # Coriolis/centrifugal coefficients
    c1 = self.m1 * self.lc1 + self.m2 * self.L1
    c2 = self.m2 * self.lc2
    c12 = self.m2 * self.L1 * self.lc2

    C = np.zeros((3, 3))

    # First row (cart equation)
    C[0, 1] = -c1 * s1 * theta1_dot
    C[0, 2] = -c2 * s2 * theta2_dot

    # Second row (pendulum 1 equation)
    C[1, 0] = -c1 * s1 * theta1_dot
    C[1, 2] = -c12 * s12 * theta2_dot

    # Third row (pendulum 2 equation)
    C[2, 0] = -c2 * s2 * theta2_dot
    C[2, 1] = c12 * s12 * theta1_dot

    return C
```

**Physical Interpretation:**

**Coriolis Force**: Apparent force due to rotation
- Example: When pendulum 1 rotates, it induces forces on cart and pendulum 2
- Term: `-c12 * sin(θ₁ - θ₂) * θ̇₂` couples pendulum velocities

**Centrifugal Force**: Outward force due to rotation
- Example: Rotating pendulum creates force pushing cart sideways
- Term: `-c1 * sin(θ₁) * θ̇₁²` pushes cart away from pendulum

## Gravity Vector

```python
def _compute_gravity_vector(self, theta1: float, theta2: float) -> np.ndarray:
    """
    Compute gravity vector G(q).

    G = -∂V/∂q where V = potential energy
    """
    s1 = np.sin(theta1)
    s2 = np.sin(theta2)

    g1 = self.m1 * self.lc1 + self.m2 * self.L1
    g2 = self.m2 * self.lc2

    return np.array([
        0,                          # No gravity on cart (horizontal)
        -g1 * self.g * s1,         # Pendulum 1 torque
        -g2 * self.g * s2          # Pendulum 2 torque
    ])
```

**Sign Convention**: Upright (θ=0) is unstable equilibrium
- Gravity torque pushes pendulum away from vertical
- Control must counteract this destabilizing torque

## Three Model Variants

### 1. Simplified Linear Model

**File**: `src/plant/simplified_dip.py`

**Assumptions:**
- Small angles: `sin(θ) ≈ θ`, `cos(θ) ≈ 1`
- Neglect second-order terms: `θ₁·θ₂ ≈ 0`, `θ̇₁² ≈ 0`
- Constant mass matrix (linearized around θ=0)

**Advantages:**
- 10-100x faster computation
- Ideal for PSO optimization (thousands of simulations)
- Analytical Jacobians available

**Limitations:**
- Accurate only near upright: `|θ₁|, |θ₂| < 5-10°`
- Cannot simulate swing-up (large angles)
- Underestimates nonlinear effects

**Code Structure:**

```python
class SimplifiedDIP:
    def compute_dynamics(self, state: np.ndarray, u: float) -> np.ndarray:
        # Extract state
        x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

        # Linearized mass matrix (constant)
        M = self._get_linearized_mass_matrix()

        # Simplified dynamics (linear in theta)
        h = self._compute_linear_terms(theta1, theta2)

        # Solve: M·q̈ = Bu - h
        B = np.array([1.0, 0.0, 0.0])
        q_ddot = np.linalg.solve(M, B * u - h)

        return np.array([x_dot, theta1_dot, theta2_dot,
                        q_ddot[0], q_ddot[1], q_ddot[2]])
```

**When to Use:**
- PSO optimization
- Initial controller testing
- Educational demonstrations
- Systems constrained to small angles

### 2. Full Nonlinear Model

**File**: `src/plant/full_dip.py`

**Features:**
- Complete trigonometric terms
- Coriolis and centrifugal effects
- Gyroscopic coupling
- Full operating range

**Code Structure:**

```python
class FullNonlinearDIP:
    def compute_dynamics(self, state: np.ndarray, u: float) -> np.ndarray:
        # Extract state
        x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

        # Configuration-dependent mass matrix
        M = self._compute_mass_matrix(theta1, theta2)

        # Coriolis/centrifugal matrix
        C = self._compute_coriolis_matrix(theta1, theta2,
                                          theta1_dot, theta2_dot)

        # Gravity vector
        G = self._compute_gravity_vector(theta1, theta2)

        # Friction
        D = np.diag([self.b_cart, self.b_joint1, self.b_joint2])

        # Input distribution
        B = np.array([1.0, 0.0, 0.0])

        # Full dynamics: M·q̈ + C·q̇ + G + D·q̇ = Bu
        q_dot = np.array([x_dot, theta1_dot, theta2_dot])
        rhs = B * u - C @ q_dot - G - D @ q_dot

        # Solve for acceleration
        q_ddot = np.linalg.solve(M, rhs)

        return np.array([x_dot, theta1_dot, theta2_dot,
                        q_ddot[0], q_ddot[1], q_ddot[2]])
```

**When to Use:**
- Final validation
- Swing-up control
- Research benchmarks
- Realistic simulations

### 3. Low-Rank Approximation

**File**: `src/plant/lowrank_dip.py`

**Method**: Proper Orthogonal Decomposition (POD)
1. Collect snapshots from full model
2. Compute SVD: `X = UΣVᵀ`
3. Retain top-k modes: `X̃ = U_k Σ_k V_kᵀ`
4. Project dynamics onto reduced basis

**Advantages:**
- 10-50x speedup vs. full model
- Preserves dominant dynamics
- Suitable for Monte Carlo studies

**Limitations:**
- Requires training data
- Accuracy depends on snapshot diversity
- May miss rare phenomena

**When to Use:**
- Large-scale parameter sweeps
- Sensitivity analysis (1000+ runs)
- Real-time applications (HIL)

## Model Accuracy Comparison

### Validation Test (MT-6 Benchmark)

**Setup:**
- Initial condition: `θ₁ = 10°`, `θ₂ = 5°`
- Controller: Classical SMC with optimized gains
- Duration: 10 seconds
- Metric: Settling time, overshoot, RMS error

**Results:**

| Model | Settling Time [s] | Overshoot [°] | RMS Error [°] | Speed [sims/sec] |
|-------|-------------------|---------------|---------------|------------------|
| Simplified | 2.31 | 4.2 | 0.12 | 450 |
| Full Nonlinear | 2.58 | 5.1 | 0.15 | 8 |
| Low-Rank (k=10) | 2.54 | 4.9 | 0.14 | 95 |

**Observations:**
1. Simplified model underestimates settling time (optimistic)
2. Full model most conservative (realistic)
3. Low-rank model good compromise (2% error, 12x speedup)

### Angle Range Validation

**Test**: Swing-up from θ₁ = 180° (hanging down)

| Model | Can Simulate? | Max Angle Error |
|-------|---------------|-----------------|
| Simplified | NO (invalid at θ>10°) | N/A |
| Full Nonlinear | YES | Reference |
| Low-Rank | YES (if trained on swing-up) | 3.5° |

**Conclusion**: Simplified model ONLY valid near upright!

## Implementation Details

### Numerical Integration

**Available Integrators** (from `config.yaml`):

```yaml
verification:
  integrators:
    - euler    # 1st order, fast, inaccurate
    - rk4      # 4th order, good balance
    - rk45     # Adaptive, most accurate
```

**Euler (1st order):**
```python
def euler_step(f, state, u, dt):
    state_dot = f(state, u)
    return state + state_dot * dt
```

**RK4 (4th order):**
```python
def rk4_step(f, state, u, dt):
    k1 = f(state, u)
    k2 = f(state + 0.5*dt*k1, u)
    k3 = f(state + 0.5*dt*k2, u)
    k4 = f(state + dt*k3, u)
    return state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
```

**RK45 (adaptive):**
- SciPy's `solve_ivp` with automatic step size
- Error control: `rtol=1e-6`, `atol=1e-9`
- Best for high-accuracy validation

**Typical Choice**: RK4 with `dt = 0.001s` (1 kHz)

### Singularity Handling

**Problem**: `M(q)` may become ill-conditioned near certain configurations.

**Solutions:**

**1. Condition Number Monitoring:**
```python
cond = np.linalg.cond(M)
if cond > threshold:
    logger.warning(f"Ill-conditioned mass matrix: κ={cond:.2e}")
```

**2. Regularized Inversion:**
```python
# Add small diagonal perturbation
M_reg = M + epsilon * np.eye(3)
M_inv = np.linalg.inv(M_reg)
```

**3. Pseudoinverse:**
```python
M_inv = np.linalg.pinv(M, rcond=1e-6)
```

**From `config.yaml`:**
```yaml
stability_monitoring:
  conditioning:
    median_threshold: 10000000.0      # Warn if median κ > 1e7
    spike_threshold: 1000000000.0     # Warn if p99 κ > 1e9
    fallback_threshold: 3             # Max pseudoinverse uses per episode
```

## Common Pitfalls and Tips

### Pitfall 1: Wrong Angle Convention

**Problem**: Sign errors in sin/cos terms.

**Our Convention**: θ = 0 at upright (unstable equilibrium)
- Gravity term: `-m·g·l·sin(θ)` (pushes away from vertical)
- Pendulum points UP when θ=0

**Alternative**: θ = 0 at hanging (stable equilibrium)
- Would require different gravity signs
- Less common for inverted pendulum control

### Pitfall 2: Inconsistent Units

**Problem**: Mixing radians and degrees.

**Solution**: ALWAYS use SI units internally:
- Angles: radians
- Angular velocity: rad/s
- Lengths: meters
- Masses: kilograms
- Forces: Newtons

**Conversion for Display:**
```python
theta_deg = np.rad2deg(theta)  # For plotting
theta_rad = np.deg2rad(theta_deg)  # From user input
```

### Pitfall 3: Ignoring Parameter Bounds

**Problem**: Unphysical parameters cause numerical issues.

**Validation** (from `src/config.py`):
```python
@validator('cart_mass')
def validate_cart_mass(cls, v):
    if v <= 0:
        raise ValueError("Cart mass must be positive")
    if v < 0.5 or v > 10.0:
        logger.warning(f"Unusual cart mass: {v} kg")
    return v

@validator('pendulum1_inertia')
def validate_inertia(cls, v, values):
    # Minimum: point mass at COM
    m = values.get('pendulum1_mass', 0.2)
    l = values.get('pendulum1_com', 0.2)
    I_min = m * l**2

    if v < I_min:
        raise ValueError(f"Inertia {v} < minimum {I_min} for point mass")
    return v
```

### Tip 1: Validate Against Known Solutions

**Test Case**: Undamped pendulum oscillation

```python
def test_conservation_of_energy():
    # No friction, no control
    config = get_config(cart_friction=0, joint1_friction=0, joint2_friction=0)

    # Initial condition: θ₁ = 10°, zero velocity
    state0 = np.array([0, 0.174, 0, 0, 0, 0])  # 10° = 0.174 rad

    # Simulate for 10 seconds
    result = simulate(state0, u=0, duration=10.0, dt=0.001)

    # Compute total energy at each timestep
    E = [kinetic_energy(s) + potential_energy(s) for s in result.states]

    # Energy should be conserved (E(t) = E(0))
    energy_drift = abs(E[-1] - E[0]) / E[0]
    assert energy_drift < 0.01  # <1% drift acceptable
```

### Tip 2: Cross-Check with Simplified Model

**Workflow:**
1. Develop controller with simplified model (fast iteration)
2. Validate with full model (realistic)
3. Compare results - should match for small angles

**Example:**
```python
# Simplified model
result_simple = simulate_simplified(state0, controller, duration=5.0)

# Full nonlinear model
result_full = simulate_full(state0, controller, duration=5.0)

# Compare
theta1_diff = np.mean(np.abs(result_simple.theta1 - result_full.theta1))
print(f"Mean θ₁ difference: {np.rad2deg(theta1_diff):.2f}°")

# Should be <1° for |θ| < 5°
assert theta1_diff < np.deg2rad(1.0)
```

## Summary and Key Takeaways

### Plant Model Fundamentals

1. **Lagrangian Mechanics**: Systematic derivation from energy
2. **Equation of Motion**: `M(q)q̈ + C(q,q̇)q̇ + G(q) = Bu`
3. **Three Variants**: Simplified (fast), Full (accurate), Low-Rank (balanced)

### Numerical Considerations

1. **Mass Matrix**: Configuration-dependent, symmetric, positive definite
2. **Conditioning**: Monitor κ(M), use regularization if needed
3. **Integration**: RK4 recommended (balance of speed/accuracy)

### Practical Implementation

1. **Model Selection**: Simplified for PSO, Full for validation
2. **Parameter Validation**: Check physical bounds
3. **Energy Conservation**: Test case for validation
4. **Cross-Checking**: Compare simplified vs. full models

### Performance Trade-offs

| Aspect | Simplified | Full | Low-Rank |
|--------|------------|------|----------|
| Speed | 10/10 | 2/10 | 7/10 |
| Accuracy (small θ) | 9/10 | 10/10 | 9/10 |
| Accuracy (large θ) | 0/10 | 10/10 | 7/10 |
| Use Case | PSO | Validation | Monte Carlo |

## Next Episode Preview

**E004: PSO Optimization** will cover:
- Particle Swarm Optimization algorithm
- Cost function design
- Constraint handling
- Robust optimization techniques
- Real performance improvements (MT-8 results)

---

**Episode Length**: ~1000 lines
**Reading Time**: 25-30 minutes
**Prerequisites**: Classical mechanics, linear algebra
**Next**: E004 - PSO Optimization
