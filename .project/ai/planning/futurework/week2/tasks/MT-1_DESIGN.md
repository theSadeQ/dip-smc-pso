# MT-1.1: Terminal SMC Design Document

**Status**: ✅ COMPLETE
**Date**: October 17, 2025
**Duration**: 2h actual

---

## 1. Mathematical Foundation

### 1.1 Nonlinear Sliding Surface

**From theory docs (lines 278-279)**:
```math
s = e + β · sign(e)|e|^α
```

**For DIP system**:
```math
s = (k1·θ̇1 + λ1·θ1) + (k2·θ̇2 + λ2·θ2) + β·sign(s_linear)|e|^α
```

where:
- `e = sqrt(θ1² + θ2²)` - Error norm (position errors only)
- `s_linear = (k1·θ̇1 + λ1·θ1) + (k2·θ̇2 + λ2·θ2)` - Linear sliding variable
- `α ∈ (0, 1)` - Convergence exponent (creates "terminal attractor")
- `β > 0` - Terminal gain parameter

**Key property** (line 287): As `|e| → 0`, the term `|e|^α` grows slower than `e`, accelerating convergence.

### 1.2 Control Law

**From theory docs (line 293)**:
```math
u = -K · sign(s)
```

**With boundary layer** (to reduce chattering):
```math
u = u_eq - K·sat(s/ε)
```

where:
- `u_eq` - Equivalent control (model-based feedforward)
- `sat(s/ε)` - Saturation function (tanh or linear)
- `ε` - Boundary layer thickness

### 1.3 Finite-Time Convergence Bound

**From theory docs (lines 301-302)**:
```math
t_reach ≤ |s(0)|^(1-α) / (β(1-α))
```

**Implications**:
- Smaller α → faster convergence (but closer to α=0 → singular behavior)
- Larger β → faster convergence
- Typical α = 0.7 provides good balance

---

## 2. Implementation Design

### 2.1 Class Structure (Following ClassicalSMC Pattern)

```python
class TerminalSMC:
    def __init__(self, gains, max_force, boundary_layer, dynamics_model, ...):
        # Validate 7 gains: [k1, k2, λ1, λ2, α, β, K]
        # Check 0 < α < 1 constraint (CRITICAL)
        # Store weakref to dynamics_model
        # Initialize boundary layer

    def compute_control(self, state, state_vars, history):
        # Compute linear sliding variable
        # Compute error norm
        # Compute nonlinear terminal term
        # Compute s = s_linear + terminal_term
        # Compute equivalent control u_eq
        # Compute switching control u_sw = -K·sat(s/ε)
        # Combine and saturate
        # Return TSMCOutput(u, (), history)

    def _compute_sliding_surface(self, state):
        # Extract state: [x, θ1, θ2, ẋ, θ̇1, θ̇2]
        # Compute s_linear (same as classical SMC)
        # Compute e_norm = sqrt(θ1² + θ2²)
        # Compute terminal term: β·sign(s_linear)|e_norm|^α
        # Return s = s_linear + terminal_term

    def _compute_equivalent_control(self, state):
        # Reuse pattern from ClassicalSMC (lines 337-417)
        # Model-based feedforward using physics matrices

    @staticmethod
    def validate_gains(gains):
        # Check length == 7
        # Check all positive
        # Check 0 < α < 1 (CRITICAL CONSTRAINT)

    # Memory management (weakref pattern)
    def cleanup(self): ...
    def __del__(self): ...

    # Properties
    @property
    def gains(self): return self._gains
    @property
    def dyn(self): return self._dynamics_ref()
```

### 2.2 Sliding Surface Computation (Core Algorithm)

```python
def _compute_sliding_surface(self, state: np.ndarray) -> float:
    """Compute nonlinear terminal sliding surface.

    Returns:
        s = (k1·θ̇1 + λ1·θ1) + (k2·θ̇2 + λ2·θ2) + β·sign(s_linear)|e|^α
    """
    _, θ1, θ2, _, θ̇1, θ̇2 = state

    # Linear sliding variable (same as classical SMC)
    s_linear = self.k1 * θ̇1 + self.lam1 * θ1 + self.k2 * θ̇2 + self.lam2 * θ2

    # Error norm (position errors only, ignoring cart position)
    e_norm = np.sqrt(θ1**2 + θ2**2)

    # Nonlinear terminal term: β·sign(s_linear)·|e|^α
    # CRITICAL: Add epsilon guard to avoid division by zero
    if e_norm > 1e-6:  # Numerical safety threshold
        terminal_term = self.beta * np.sign(s_linear) * (e_norm ** self.alpha)
    else:
        # Near equilibrium: disable terminal term
        terminal_term = 0.0

    return s_linear + terminal_term
```

**Design rationale**:
- Use position errors only (θ1, θ2) for error norm (consistent with theory)
- Epsilon guard (1e-6) prevents numerical instability near equilibrium
- Terminal term disabled when errors < 1e-6 (safe fallback)

### 2.3 Gain Validation (Critical Constraint)

```python
@staticmethod
def validate_gains(gains):
    """Validate 7 gains: [k1, k2, λ1, λ2, α, β, K]"""
    arr = np.asarray(gains, dtype=float).ravel()

    # Check length
    if arr.size != 7:
        raise ValueError("Terminal SMC requires 7 gains: [k1, k2, λ1, λ2, α, β, K]")

    # Extract α (5th gain)
    α = float(arr[4])

    # CRITICAL: Validate 0 < α < 1 (theory requirement)
    if not (0 < α < 1):
        raise ValueError(f"Terminal SMC requires 0 < α < 1, got α={α}")

    # Positivity check will be done in __init__ via require_positive
```

---

## 3. Gain Specifications

### 3.1 Gain Parameters (7 total)

| Index | Symbol | Name | Physical Meaning | Range | Default |
|-------|--------|------|------------------|-------|---------|
| 0 | k1 | Position gain 1 | Velocity error θ̇1 | [2.0, 30.0] | 20.0 |
| 1 | k2 | Position gain 2 | Velocity error θ̇2 | [2.0, 30.0] | 15.0 |
| 2 | λ1 | Velocity gain 1 | Position error θ1 | [2.0, 10.0] | 12.0 |
| 3 | λ2 | Velocity gain 2 | Position error θ2 | [0.2, 5.0] | 8.0 |
| 4 | α | Convergence exponent | Terminal attractor strength | (0.5, 0.95) | 0.7 |
| 5 | β | Terminal gain | Terminal term scale | [1.0, 20.0] | 10.0 |
| 6 | K | Switching gain | Robust control authority | [5.0, 50.0] | 35.0 |

**Default gains**: `[20.0, 15.0, 12.0, 8.0, 0.7, 10.0, 35.0]`

### 3.2 Constraint Summary

**Strict positivity** (all gains > 0):
- k1, k2, λ1, λ2 > 0 (sliding surface stability)
- β > 0 (terminal term must be positive)
- K > 0 (switching gain must be positive)

**Fractional exponent** (CRITICAL):
- 0 < α < 1 (strict inequality, no equality allowed)
- Typical range: [0.5, 0.9]
- α = 0.7 recommended (good balance)
- α → 0: Faster but singular behavior
- α → 1: Approaches linear (loses terminal advantage)

### 3.3 PSO Bounds

For PSO optimization:
```python
min_bounds = [2.0, 2.0, 2.0, 0.2, 0.5, 1.0, 5.0]
max_bounds = [30.0, 30.0, 10.0, 5.0, 0.95, 20.0, 50.0]
```

**Note**: α upper bound is 0.95 (not 1.0) to ensure strict inequality.

---

## 4. Expected Performance

### 4.1 Convergence Speed

**From theory (line 307)**:
- **Target**: 30-50% faster than classical SMC
- **Measured as**: Settling time (time for |θ1|, |θ2| < 0.01)

**Mechanism**: Nonlinear term |e|^α accelerates as error decreases.

### 4.2 Overshoot

**From theory (line 308)**:
- **Expected**: Reduced due to nonlinear damping
- **Comparison**: Terminal ≤ Classical

### 4.3 Chattering

**From theory (line 309)**:
- **Expected**: Similar to classical SMC
- **Requires**: Boundary layer (ε = 0.02 typical)
- **Mitigation**: sat(s/ε) instead of sign(s)

---

## 5. Implementation Checklist

### 5.1 Files to Create

- [ ] `src/controllers/tsmc_smc.py` (~300 lines)
  - Class definition
  - __init__ with 7-gain validation
  - _compute_sliding_surface (nonlinear term)
  - compute_control (main control loop)
  - _compute_equivalent_control (reuse ClassicalSMC pattern)
  - validate_gains (7 gains, α constraint)
  - cleanup, __del__ (weakref pattern)
  - Properties: gains, dyn

### 5.2 Key Implementation Points

1. **Alpha constraint** (line 4 of gains):
   ```python
   if not (0 < self.alpha < 1):
       raise ValueError("Terminal SMC requires 0 < alpha < 1")
   ```

2. **Epsilon guard** (in _compute_sliding_surface):
   ```python
   if e_norm > 1e-6:
       terminal_term = self.beta * np.sign(s_linear) * (e_norm ** self.alpha)
   else:
       terminal_term = 0.0
   ```

3. **Weakref pattern** (from ClassicalSMC):
   ```python
   if dynamics_model is not None:
       self._dynamics_ref = weakref.ref(dynamics_model)
   else:
       self._dynamics_ref = lambda: None
   ```

4. **Saturation** (final control):
   ```python
   u_saturated = float(np.clip(u, -self.max_force, self.max_force))
   ```

---

## 6. Risk Assessment

### 6.1 Technical Risks

| Risk | Probability | Mitigation |
|------|------------|------------|
| **Numerical instability** near e=0 | Medium | Epsilon guard (e_norm > 1e-6) |
| **α constraint violation** | Low | Explicit check in validate_gains |
| **Terminal term sign error** | Low | Use sign(s_linear) consistently |
| **Convergence slower than expected** | Medium | Tune α and β manually if PSO fails |

### 6.2 Implementation Risks

| Risk | Probability | Mitigation |
|------|------------|------------|
| **Weakref pattern incorrect** | Low | Follow ClassicalSMC pattern exactly |
| **Gain unpacking order wrong** | Low | Document order clearly, add comment |
| **Equivalent control reuse fails** | Low | Copy-paste from ClassicalSMC |

---

## 7. Testing Strategy (Preview for MT-1.3)

### 7.1 Unit Tests

1. **Initialization**: Valid 7 gains → no errors
2. **Gain validation**: 6 gains → ValueError, α=0 → ValueError, α=1 → ValueError
3. **Sliding surface**: Compute s for known state → check nonlinear term present
4. **Alpha constraint**: α=0.5, 0.7, 0.9 → valid; α=0, 1, 1.5 → invalid

### 7.2 Integration Tests

1. **Compute control**: Valid state → returns TSMCOutput with u in [-150, 150]
2. **Saturation**: Large errors → u saturates to ±150
3. **History tracking**: Multiple calls → history accumulates sigma, u_eq, u_sw, u

### 7.3 Performance Tests

1. **Convergence speed**: Terminal SMC vs Classical SMC settling time → 30-50% faster
2. **Overshoot**: Terminal ≤ Classical
3. **Chattering**: Similar RMS |du/dt|

---

## 8. Quality Gates (MT-1.1)

**QG-1 Checklist**:
- [x] Sliding surface equation validated against theory
- [x] Gain bounds defined (7 gains with ranges)
- [x] Alpha constraint design (0 < α < 1)
- [x] Epsilon guard design (e_norm > 1e-6)
- [x] Implementation pattern established (following ClassicalSMC)
- [x] Design document created

**Decision**: ✅ **GO** to MT-1.2 (Implementation)

**Confidence**: **HIGH** - Theory clear, pattern established, risks identified and mitigated.

---

## 9. Next Steps

**MT-1.2: Core Implementation** (4 hours)
1. Create `src/controllers/tsmc_smc.py`
2. Implement class skeleton + __init__ (Hour 1)
3. Implement _compute_sliding_surface with nonlinear term (Hour 2)
4. Implement compute_control + _compute_equivalent_control (Hour 3)
5. Implement utilities (validate_gains, cleanup, properties) (Hour 4)

**Deliverable**: Functional Terminal SMC controller (~300 lines)

---

**Design Completed**: October 17, 2025
**Status**: ✅ READY FOR IMPLEMENTATION
**Next Task**: MT-1.2 (Core Implementation)
