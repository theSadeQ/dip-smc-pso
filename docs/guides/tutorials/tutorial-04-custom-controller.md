# Tutorial 04: Custom Controller Development **Level:** Advanced
**Duration:** 90-120 minutes
**Prerequisites:**
- Completed [Tutorial 01: Your First Simulation](tutorial-01-first-simulation.md)
- Completed [Tutorial 02: Controller Comparison](tutorial-02-controller-comparison.md)
- Python programming experience
- Understanding of SMC theory (recommended) ## Learning Objectives By the end of this tutorial, you will: - [ ] Understand the controller interface and architecture
- [ ] Implement a custom SMC variant from scratch
- [ ] Add gain validation and error handling
- [ ] Integrate your controller with the factory system
- [ ] Add configuration support in `config.yaml`
- [ ] Test and validate your custom controller
- [ ] Optimize custom controller gains using PSO --- ## Part 1: Controller Architecture Overview ### The Controller Interface All controllers in this framework implement a **consistent interface**: ```python
# example-metadata:
# runnable: false class MyCustomController: def __init__(self, gains, max_force, **kwargs): """Initialize controller with gains and parameters.""" pass def compute_control(self, state, state_vars, history): """ Compute control signal for current state. Parameters ---------- state : np.ndarray State vector [x, dx, θ₁, dθ₁, θ₂, dθ₂] state_vars : dict Controller-specific internal state history : dict Historical data for multi-step algorithms Returns ------- control : float Control input (force applied to cart) state_vars : dict Updated internal state history : dict Updated history """ pass def initialize_history(self) -> dict: """Initialize history buffer for controller.""" return {} def cleanup(self): """Clean up resources (optional).""" pass
``` ### Key Components **1. Gains (`__init__`)**
- Controller-specific parameters (surface gains, switching gains, adaptation rates, etc.)
- Must be validated for physical plausibility **2. State Variables (`state_vars`)**
- Controller internal state that persists between timesteps
- Examples: adaptive gains, integral terms, filter states **3. History (`history`)**
- Multi-step data (previous states, controls)
- Used for integral control, finite-difference derivatives, etc. **4. Control Computation (`compute_control`)**
- Core control law implementation
- Returns control signal + updated state_vars + updated history --- ## Part 2: Implementing a Terminal SMC (TSMC) ### What is Terminal SMC? **Terminal Sliding Mode Control** uses a **nonlinear sliding surface** with fractional powers to achieve **finite-time convergence** (faster than asymptotic). **Classical SMC Sliding Surface:**
```
s = k₁·θ₁ + k₂·dθ₁ + λ₁·θ₂ + λ₂·dθ₂ (linear in errors)
``` **Terminal SMC Sliding Surface:**
```
s = k₁·θ₁ + k₂·sign(dθ₁)·|dθ₁|^α + λ₁·θ₂ + λ₂·sign(dθ₂)·|dθ₂|^β
``` where `α, β ∈ (0, 1)` (e.g., 0.5, 0.7) create the terminal attractor. **Benefits:**
- **Finite-time convergence** (reaches equilibrium in finite time, not just asymptotically)
- **Faster response** near equilibrium (stronger control when errors are small) **Challenges:**
- **Singularity avoidance** (control can blow up if not handled carefully)
- **More gains to tune** (4 surface gains + 2 exponents) > **📚 Theory Background:** For SMC foundations before implementing custom controllers:
> - [SMC Theory Guide](../theory/smc-theory.md) - Lyapunov stability, sliding surfaces, design guidelines ### Step 1: Create the Controller File Create `src/controllers/smc/terminal_smc.py`: ```python
# example-metadata:
# runnable: false #======================================================================================\\\
#======================== src/controllers/smc/terminal_smc.py ========================\\\
#======================================================================================\\\ """
Terminal Sliding Mode Controller for double-inverted pendulum. Implements nonlinear terminal sliding surface for finite-time convergence.
""" import numpy as np
import logging
import weakref
from typing import TYPE_CHECKING, List, Tuple, Dict, Optional, Union, Sequence from ...utils import saturate, TerminalSMCOutput if TYPE_CHECKING: from ...plant.models.dynamics import DoubleInvertedPendulum logger = logging.getLogger(__name__) class TerminalSMC: """ Terminal Sliding Mode Controller with finite-time convergence. Uses nonlinear terminal sliding surface with fractional exponents to achieve faster convergence than classical SMC. Parameters ---------- gains : array-like [k1, k2, λ1, λ2, K, α, β] - k1, k2, λ1, λ2: sliding surface gains (positive) - K: switching gain (positive) - α, β: terminal exponents in (0, 1) for finite-time convergence max_force : float Maximum control force (N) boundary_layer : float Boundary layer thickness for chattering reduction dynamics_model : DoubleInvertedPendulum, optional
        Dynamics model for equivalent control (if None, uses robust control only)
    singularity_epsilon : float, default=1e-3
        Small value to avoid singularity when velocities near zero """ def __init__( self, gains: Union[Sequence[float], np.ndarray], max_force: float, boundary_layer: float, dynamics_model: Optional["DoubleInvertedPendulum"] = None, singularity_epsilon: float = 1e-3, switch_method: str = "tanh", ): # Validate gain count if len(gains) != 7: raise ValueError( f"Terminal SMC requires 7 gains [k1,k2,λ1,λ2,K,α,β], got {len(gains)}" ) # Extract and validate gains self.k1, self.k2, self.lam1, self.lam2, self.K, self.alpha, self.beta = gains # Validate gain constraints if self.k1 <= 0 or self.k2 <= 0 or self.lam1 <= 0 or self.lam2 <= 0: raise ValueError("Surface gains k1, k2, λ1, λ2 must be positive") if self.K <= 0: raise ValueError("Switching gain K must be positive") if not (0 < self.alpha < 1): raise ValueError(f"Terminal exponent α must be in (0,1), got {self.alpha}") if not (0 < self.beta < 1): raise ValueError(f"Terminal exponent β must be in (0,1), got {self.beta}") # Store parameters self.max_force = max_force self.boundary_layer = boundary_layer self.singularity_epsilon = singularity_epsilon self.switch_method = switch_method # Store dynamics model reference (weakref to avoid circular reference) if dynamics_model is not None: self._dynamics_ref = weakref.ref(dynamics_model) else: self._dynamics_ref = lambda: None logger.info( f"Initialized Terminal SMC: gains={gains}, max_force={max_force}, " f"boundary_layer={boundary_layer}" ) @property def dyn(self): """Access dynamics model via weakref.""" if self._dynamics_ref is not None: return self._dynamics_ref() return None def compute_sliding_surface(self, state: np.ndarray) -> float: """ Compute terminal sliding surface. s = k₁·θ₁ + k₂·sign(dθ₁)·|dθ₁|^α + λ₁·θ₂ + λ₂·sign(dθ₂)·|dθ₂|^β Parameters ---------- state : np.ndarray [x, dx, θ₁, dθ₁, θ₂, dθ₂] Returns ------- s : float Sliding surface value """ _, _, theta1, dtheta1, theta2, dtheta2 = state # Terminal terms with singularity avoidance # Add small epsilon to avoid division by zero term1 = np.sign(dtheta1) * np.abs(dtheta1 + self.singularity_epsilon) ** self.alpha term2 = np.sign(dtheta2) * np.abs(dtheta2 + self.singularity_epsilon) ** self.beta # Sliding surface s = self.k1 * theta1 + self.k2 * term1 + self.lam1 * theta2 + self.lam2 * term2 return s def switching_function(self, s: float) -> float: """ Continuous approximation to sign function. Parameters ---------- s : float Sliding surface value Returns ------- switch : float Switching function output in [-1, 1] """ if self.switch_method == "tanh": return np.tanh(s / self.boundary_layer) elif self.switch_method == "linear": return saturate(s / self.boundary_layer, -1.0, 1.0) else: raise ValueError(f"Unknown switch method: {self.switch_method}") def compute_control( self, state: np.ndarray, state_vars: Optional[Dict] = None, history: Optional[Dict] = None, ) -> Tuple[float, Dict, Dict]: """ Compute terminal SMC control law. Parameters ---------- state : np.ndarray State vector [x, dx, θ₁, dθ₁, θ₂, dθ₂] state_vars : dict, optional Controller internal state (unused for terminal SMC) history : dict, optional Historical data (unused for terminal SMC) Returns ------- control : float Control input (force) state_vars : dict Updated state variables history : dict Updated history """ # Initialize if None if state_vars is None: state_vars = {} if history is None: history = self.initialize_history() # Compute sliding surface s = self.compute_sliding_surface(state) # Compute switching function switch = self.switching_function(s) # Control law: u = -K·switch(s) # (Simplified: no equivalent control for tutorial simplicity) control = -self.K * switch # Saturate to max force control = saturate(control, -self.max_force, self.max_force) # Log for debugging logger.debug(f"Terminal SMC: s={s:.4f}, switch={switch:.4f}, u={control:.4f}") return control, state_vars, history def initialize_history(self) -> Dict: """Initialize empty history (terminal SMC is memoryless).""" return {} def cleanup(self): """Clean up resources.""" self._dynamics_ref = None logger.debug("Terminal SMC cleaned up") def __del__(self): """Destructor for automatic cleanup.""" self.cleanup()
``` ### Step 2: Create Output Dataclass Add to `src/utils/types/control_types.py`: ```python
@dataclass(frozen=True)
class TerminalSMCOutput: """Output from Terminal SMC controller.""" control: float sliding_surface: float switching_function: float terminal_term1: float # sign(dθ₁)·|dθ₁|^α terminal_term2: float # sign(dθ₂)·|dθ₂|^β
``` --- ## Part 3: Factory Integration ### Step 1: Add to SMC Factory Edit `src/controllers/factory/smc_factory.py`: ```python
# example-metadata:
# runnable: false from ..smc.terminal_smc import TerminalSMC # Add import class SMCType(str, Enum): CLASSICAL = "classical" ADAPTIVE = "adaptive" SUPER_TWISTING = "super_twisting" HYBRID = "hybrid" TERMINAL = "terminal" # New controller type # Update GAIN_SPECIFICATIONS
GAIN_SPECIFICATIONS = { # ... existing specs ... SMCType.TERMINAL: GainSpecification( controller_type=SMCType.TERMINAL, n_gains=7, gain_names=["k1", "k2", "lambda1", "lambda2", "K", "alpha", "beta"], bounds=[(0.1, 50.0), (0.1, 50.0), (0.1, 50.0), (0.1, 50.0), (1.0, 200.0), (0.1, 0.9), (0.1, 0.9)], description="Terminal SMC with nonlinear sliding surface" ),
} # Update create_controller method
@staticmethod
def create_controller( controller_type: SMCType, config: SMCConfig, dynamics_model: Optional[Any] = None,
) -> Any: """Create SMC controller instance.""" # ... existing code ... elif controller_type == SMCType.TERMINAL: from ..smc.terminal_smc import TerminalSMC return TerminalSMC( gains=config.gains, max_force=config.max_force, boundary_layer=config.boundary_layer, dynamics_model=dynamics_model, singularity_epsilon=getattr(config, 'singularity_epsilon', 1e-3), switch_method=getattr(config, 'switch_method', 'tanh'), ) # ... rest of code ...
``` ### Step 2: Add Configuration Support Edit `config.yaml`: ```yaml
controllers: # ... existing controllers ... terminal_smc: gains: [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7] # [k1, k2, λ1, λ2, K, α, β] max_force: 100.0 boundary_layer: 0.01 singularity_epsilon: 0.001 # Avoid singularity switch_method: "tanh"
``` --- ## Part 4: Testing Your Custom Controller ### Manual Testing ```bash
# Test terminal SMC with default configuration
python simulate.py --ctrl terminal_smc --plot
``` **Expected Output:**
- Simulation should complete without errors
- Plot should show state convergence
- Control signal should be bounded by max_force ### Unit Testing Create `tests/test_controllers/test_terminal_smc.py`: ```python
import pytest
import numpy as np
from src.controllers.smc.terminal_smc import TerminalSMC class TestTerminalSMC: """Unit tests for Terminal SMC controller.""" def test_initialization_valid_gains(self): """Test controller initializes with valid gains.""" gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7] controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) assert controller.k1 == 10.0 assert controller.alpha == 0.5 assert controller.beta == 0.7 def test_initialization_invalid_gain_count(self): """Test ValueError raised for wrong number of gains.""" gains = [10.0, 8.0, 15.0] # Only 3 gains with pytest.raises(ValueError, match="7 gains"): TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) def test_initialization_invalid_exponents(self): """Test ValueError for invalid terminal exponents.""" gains = [10.0, 8.0, 15.0, 12.0, 50.0, 1.5, 0.7] # α > 1 with pytest.raises(ValueError, match="must be in"): TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) def test_sliding_surface_computation(self): """Test sliding surface calculation.""" gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7] controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) state = np.array([0.0, 0.0, 0.1, 0.0, 0.15, 0.0]) s = controller.compute_sliding_surface(state) # s = k1·θ1 + k2·0 + λ1·θ2 + λ2·0 = 10*0.1 + 15*0.15 = 3.25 assert abs(s - 3.25) < 0.01 def test_control_computation(self): """Test control signal computation.""" gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7] controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) state = np.array([0.0, 0.0, 0.1, 0.0, 0.15, 0.0]) control, state_vars, history = controller.compute_control(state, {}, {}) # Control should be computed and bounded assert isinstance(control, (float, np.floating)) assert abs(control) <= 100.0 # max_force def test_control_saturation(self): """Test control saturation at max_force.""" gains = [10.0, 8.0, 15.0, 12.0, 500.0, 0.5, 0.7] # Very high K controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) state = np.array([0.0, 0.0, 0.5, 0.0, 0.6, 0.0]) # Large errors control, _, _ = controller.compute_control(state, {}, {}) # Control should saturate at max_force assert abs(control) == 100.0 def test_cleanup(self): """Test resource cleanup.""" gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7] controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01) controller.cleanup() # Dynamics reference should be None after cleanup assert controller._dynamics_ref is None
``` **Run tests:**
```bash
pytest tests/test_controllers/test_terminal_smc.py -v
``` --- ## Part 5: PSO Optimization of Custom Controller ### Configure PSO Bounds Edit `config.yaml`: ```yaml
pso: # Terminal SMC specific bounds terminal_smc_bounds: - [0.1, 50.0] # k₁ - [0.1, 50.0] # k₂ - [0.1, 50.0] # λ₁ - [0.1, 50.0] # λ₂ - [1.0, 200.0] # K - [0.1, 0.9] # α (must be in (0,1)) - [0.1, 0.9] # β (must be in (0,1))
``` ### Run PSO Optimization ```bash
# Optimize terminal SMC gains
python simulate.py --ctrl terminal_smc --run-pso --save gains_terminal_optimized.json
``` ### Compare with Classical SMC ```bash
# Test optimized terminal SMC
python simulate.py --load gains_terminal_optimized.json --plot --save results_terminal.json # Compare with classical SMC
python -c "
import json terminal = json.load(open('results_terminal.json'))
classical = json.load(open('results_classical.json')) # From previous tutorial print('Performance Comparison:')
print(f'Terminal SMC ISE: {terminal[\"metrics\"][\"ise\"]:.4f}')
print(f'Classical SMC ISE: {classical[\"metrics\"][\"ise\"]:.4f}')
print(f'Improvement: {(1 - terminal[\"metrics\"][\"ise\"]/classical[\"metrics\"][\"ise\"])*100:.1f}%')
"
``` **Expected Learning:**
- Terminal SMC should achieve faster convergence near equilibrium
- May have similar or slightly better ISE than classical SMC
- Exponents α, β control convergence speed vs smoothness --- ## Part 6: Advanced Customization ### Adding Equivalent Control For better performance, add model-based equivalent control: ```python
# example-metadata:
# runnable: false def compute_equivalent_control(self, state: np.ndarray) -> float: """ Compute model-based equivalent control. For terminal SMC, this requires computing: u_eq = - (L·M⁻¹·B)⁻¹ · (L·M⁻¹·C + ds/dt) where s is the terminal sliding surface. """ if self.dyn is None: return 0.0 # No model available # Get system matrices M = self.dyn.mass_matrix(state) C = self.dyn.coriolis_centrifugal(state) B = self.dyn.control_matrix() # Compute L (gradient of sliding surface w.r.t. state) L = self.compute_surface_gradient(state) # Solve for u_eq (requires matrix operations) try: M_inv = np.linalg.inv(M) LMB = L @ M_inv @ B if abs(LMB) < 1e-6: # Singularity check return 0.0 u_eq = -(1 / LMB) * (L @ M_inv @ C) return saturate(u_eq, -self.max_force, self.max_force)

    except np.linalg.LinAlgError:
        return 0.0  # Fallback to robust control only
```

### Adding State Variables (e.g., Integral Term)

```python
# example-metadata:
# runnable: false def __init__(self, ...): # ... existing code ... self.use_integral = True self.k_integral = 2.0 # Integral gain def compute_control(self, state, state_vars, history): # Initialize integral term if not present if 'integral_s' not in state_vars: state_vars['integral_s'] = 0.0 # Compute sliding surface s = self.compute_sliding_surface(state) # Update integral term dt = 0.01 # Get from config state_vars['integral_s'] += s * dt # Control law with integral term control = -self.K * self.switching_function(s) - self.k_integral * state_vars['integral_s'] # Saturate control = saturate(control, -self.max_force, self.max_force) return control, state_vars, history
``` --- ## Part 7: Best Practices ### 1. Gain Validation **Always validate gains in `__init__`:** ```python
# example-metadata:
# runnable: false def __init__(self, gains, ...): # Check count if len(gains) != expected_count: raise ValueError(f"Expected {expected_count} gains, got {len(gains)}") # Check bounds if any(g < 0 for g in gains[:4]): # Surface gains must be positive raise ValueError("Surface gains must be non-negative") # Check constraints (e.g., exponents in (0,1)) if not (0 < alpha < 1): raise ValueError(f"Exponent α must be in (0,1), got {alpha}")
``` ### 2. Numerical Robustness **Avoid singularities:** ```python
# Bad: Division by zero
term = dtheta ** alpha # Good: Add small epsilon
term = np.sign(dtheta) * (np.abs(dtheta) + 1e-6) ** alpha
``` **Matrix inversion safety:** ```python
try: M_inv = np.linalg.inv(M)
except np.linalg.LinAlgError:
    logger.warning("Singular matrix, using robust control only")
    return 0.0  # Fallback
```

### 3. Logging and Debugging

```python
# example-metadata:
# runnable: false import logging
logger = logging.getLogger(__name__) def compute_control(self, state, ...): s = self.compute_sliding_surface(state) logger.debug(f"Sliding surface: s={s:.4f}") control = ... logger.debug(f"Control output: u={control:.4f}") return control, state_vars, history
``` ### 4. Memory Management ```python
def cleanup(self): """Explicit cleanup for long-running processes.""" self._dynamics_ref = None logger.debug(f"{self.__class__.__name__} cleaned up") def __del__(self): """Automatic cleanup on garbage collection.""" self.cleanup()
``` --- ## Part 8: Exercise: Implement Fast Terminal SMC **Challenge:** Implement **Fast Terminal SMC** (FTSMC), which uses a different sliding surface: ```
s = θ₁ + β₁·sign(dθ₁)·|dθ₁|^α + θ₂ + β₂·sign(dθ₂)·|dθ₂|^γ
``` **Requirements:**
1. Create `src/controllers/smc/fast_terminal_smc.py`
2. Add to factory with type `SMCType.FAST_TERMINAL`
3. Add configuration to `config.yaml`
4. Write unit tests
5. Run PSO optimization
6. Compare performance with Terminal SMC and Classical SMC **Expected Learning:**
- Understand how different sliding surface designs affect performance
- Practice the full controller development workflow
- Gain intuition for SMC design choices --- ## Summary **Controller Development Workflow:** 1. **Design:** Define control law mathematically
2. **Implement:** Create Python class with standard interface
3. **Validate:** Add gain checking and error handling
4. **Integrate:** Add to factory and configuration
5. **Test:** Write unit tests and manual testing
6. **Optimize:** Use PSO to tune gains
7. **Compare:** Benchmark against existing controllers **Key Takeaways:** - Controllers must implement `compute_control(state, state_vars, history)`
- Always validate gains in `__init__` (count, bounds, constraints)
- Use weakref for dynamics model to avoid circular references
- Add logging for debugging
- Write unit tests
- Use PSO for automatic gain tuning **When to Create Custom Controllers:** ✅ Research on novel SMC variants
✅ Application-specific requirements (constraints, objectives)
✅ Comparing different control strategies
✅ Educational purposes --- ## Next Steps **Next Tutorial:** [Tutorial 05: Research Workflows](tutorial-05-research-workflow.md) - End-to-end project from theory to publication **Related Guides:**
- [Controllers API](../api/controllers.md): Factory integration and controller interfaces
- [Testing & Validation How-To](../how-to/testing-validation.md): testing strategies **Theory & Foundations:**
- [SMC Theory Guide](../theory/smc-theory.md): Design principles for custom controllers - Practical design guidelines - Gain selection via pole placement - Robustness analysis - Classical vs Super-Twisting comparison **Advanced Topics:**
- Adaptive laws and parameter estimation
- Observer design for state estimation
- Disturbance estimation and rejection
- Real hardware deployment (coming soon) **Congratulations!** You can now design and implement custom SMC controllers for the DIP system.
