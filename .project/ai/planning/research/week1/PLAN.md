# Week 1 Research Execution Plan

**Created**: October 17, 2025
**Duration**: 3 days (10 hours total)
**Goal**: Complete 5 foundational research tasks to build momentum for 12-week research roadmap
**Status**: READY TO EXECUTE

---

## Executive Summary

Week 1 focuses on **quick wins** and **foundational tools** that enable all subsequent research work. The 5 tasks establish baseline performance, document existing theory, add quantitative metrics, improve PSO convergence by 30%, and provide visual feedback.

**Success Metrics**:
- 5 tasks completed (QW-2, QW-1, QW-4, MT-3, QW-3)
- Baseline performance matrix generated (7 controllers × 4 metrics)
- SMC theory documented (+400 lines covering 9 controller types)
- Chattering metrics module operational (~150 lines)
- PSO converges 30% faster (35 vs 50 generations)
- Convergence plots generated and integrated

**Impact**: Unblocks Week 2-4 work (new controllers MT-1, MT-2 depend on QW-1 complete)

---

## Task Overview

| Task | Description | Effort | Priority | Deliverable |
|------|-------------|--------|----------|-------------|
| **QW-2** | Run existing benchmarks | 1h | START HERE | Baseline performance CSV |
| **QW-1** | Document SMC theory | 2h | High | +400 lines theory docs |
| **QW-4** | Add chattering metrics | 2h | High | Chattering analysis module |
| **MT-3** | Adaptive inertia PSO | 3h | HIGHEST ROI | 30% faster convergence |
| **QW-3** | Visualize PSO convergence | 2h | Medium | Convergence plots |

**Total**: 10 hours over 3 days

---

## Task 1: QW-2 - Run Existing Benchmarks (1 hour)

### Why Start Here?
- **Highest visibility**: Immediate, measurable result
- **Lowest effort**: Existing tests, just run + analyze
- **Quick win**: Builds momentum for Week 1

### Current State
- Benchmark tests exist: `tests/test_benchmarks/core/test_performance.py`
- 3 controllers benchmarked: Classical SMC, STA-SMC, Adaptive SMC
- Metrics: compute_control speed, simulation throughput, convergence time

### What to Do

**Step 1: Run benchmarks** (30 minutes)
```bash
# Run all controller benchmarks
pytest tests/test_benchmarks/ --benchmark-only --benchmark-autosave

# Run specific performance tests
pytest tests/test_benchmarks/core/test_performance.py -v --benchmark-only

# Generate JSON output for analysis
pytest tests/test_benchmarks/ --benchmark-only --benchmark-json=week1/results/benchmarks.json
```

**Step 2: Generate performance matrix** (30 minutes)
- Parse benchmark results
- Create performance matrix: 7 controllers × 4 metrics
  - Compute control time (ms)
  - Simulation throughput (steps/s)
  - Convergence time (s)
  - Control effort (RMS force)
- Save to `week1/results/baseline_performance.csv`

### Expected Output

```csv
controller,compute_ms,throughput_steps_per_s,convergence_s,rms_force_N
classical_smc,0.15,8500,0.42,45.2
sta_smc,0.18,7200,0.38,42.1
adaptive_smc,0.22,6800,0.45,48.7
...
```

### Success Criteria
- [x] Benchmarks run without errors
- [x] Performance matrix CSV generated
- [x] All 7 controllers tested (or document missing ones)
- [x] Results saved to week1/results/

### Files Modified/Created
- **Read**: tests/test_benchmarks/core/test_performance.py (existing)
- **Create**: week1/results/baseline_performance.csv (NEW)
- **Create**: week1/results/benchmarks.json (NEW, optional)

---

## Task 2: QW-1 - Document Existing SMC Theory (2 hours)

### Why Critical?
- **Foundation for MT-1, MT-2**: Cannot implement Terminal/Integral SMC without theory documentation
- **Blocks Week 2 work**: MT-1 (Terminal SMC, 10h) depends on QW-1 complete
- **Research contribution**: Publication-quality mathematical formulations

### Current State
- Theory doc exists: `docs/theory/smc_theory_complete.md` (~170 lines)
- Covers: Classical SMC, Super-Twisting, Adaptive SMC (partial)
- Missing: Hybrid SMC, Swing-Up, Terminal SMC, Integral SMC, HOSM formulations

### What to Do

**Step 1: Read existing theory doc** (15 minutes)
```bash
code docs/theory/smc_theory_complete.md
```
- Understand current structure (sections, equation style, LaTeX format)
- Identify gaps for 7 existing controllers + 2 planned

**Step 2: Add formulations for existing controllers** (60 minutes)

**Classical SMC** (already documented, verify completeness):
- Sliding surface: `s = k1*θ1 + k2*θ̇1 + λ1*θ2 + λ2*θ̇2`
- Control law: `u = u_eq + u_sw = -K*tanh(s/ε)`
- Boundary layer: `ε = 0.02` (chattering reduction)

**Super-Twisting Algorithm** (expand existing section):
- Sliding surface: Same as classical
- Control law: `u = -α|s|^{0.5}*sign(s) - ∫β*sign(s)dt`
- Gains: `[α, β, k1, k2, λ1, λ2]` with constraint `α > 0, β > 0`

**Adaptive SMC** (complete missing details):
- Sliding surface: Same as classical
- Adaptive gain: `K̂̇ = γ*|s|` (adaptation law)
- Control law: `u = -K̂*sign(s)` where `K̂` adapts online
- Leak rate: `K̂̇ = γ*|s| - leak*K̂` (prevents drift)

**Hybrid Adaptive STA-SMC** (NEW section):
- Modular design: Adaptive + STA combined
- Switching logic: |s| > threshold → Classical, |s| ≤ threshold → STA
- Gains: `[k1, k2, λ, K_adaptive]` (4 gains)

**Swing-Up SMC** (NEW section):
- Energy-based control for large angles (|θ| > π/4)
- Energy error: `E_err = E - E_desired`
- Control law: `u = k_energy * E_err * sign(θ̇) + u_balance`

**Step 3: Add formulations for planned controllers** (45 minutes)

**Terminal Sliding Mode Control (TSMC)** - **PLAN section**:
- Nonlinear sliding surface: `s = x + β*sign(x)|x|^α` where `0 < α < 1`
- Finite-time convergence (faster than asymptotic SMC)
- Control law: `u = -K*sign(s)`
- Gains: `[k1, k2, λ1, λ2, α, β, K]` (7 gains)
- **Reference**: Feng et al. (2002), Yu & Man (1998)

**Integral Sliding Mode Control (ISMC)** - **PLAN section**:
- Sliding surface with integral term: `s = x + ∫σ(x)dt`
- Eliminates reaching phase (system starts on sliding surface)
- Better disturbance rejection (integral action)
- Control law: `u = u_eq + u_sw` with integral compensation
- Gains: `[k1, k2, λ1, λ2, K, kd, ki]` (7 gains)
- **Reference**: Utkin & Shi (1996)

**Higher-Order SMC (HOSM)** - **PLAN section**:
- Generalization beyond super-twisting (order ≥ 3)
- Arbitrary-order differentiator, twisting algorithm
- Gains: Variable (8-10 gains depending on order)
- **Reference**: Levant (2003, 2005)

### Expected Output

**Updated docs/theory/smc_theory_complete.md** (~170 → ~570 lines, +400 lines):
```markdown
## Classical Sliding Mode Control
### Sliding Surface Design
### Control Law
### Stability Analysis (Lyapunov)

## Super-Twisting Algorithm
### Motivation (chattering reduction)
### Control Law
### Parameter Selection

## Adaptive SMC
### Parameter Uncertainty Model
### Adaptation Law
### Stability Proof

## Hybrid Adaptive STA-SMC
### Modular Design
### Switching Logic
### Gain Configuration

## Swing-Up SMC
### Energy-Based Control
### Control Law

## [PLAN] Terminal SMC
### Finite-Time Convergence
### Nonlinear Sliding Surface
### Expected Performance

## [PLAN] Integral SMC
### Reaching Phase Elimination
### Disturbance Rejection
### Expected Performance

## [PLAN] Higher-Order SMC
### Generalization
### Arbitrary-Order Design
```

### Success Criteria
- [x] 7 existing controllers fully documented (equations + gains + references)
- [x] 2 planned controllers documented (PLAN sections with expected formulations)
- [x] Math renders correctly (LaTeX equations in Markdown)
- [x] +400 lines added (~170 → ~570 lines)
- [x] Ready for MT-1, MT-2 implementation (Week 2)

### Files Modified
- **Update**: docs/theory/smc_theory_complete.md (+400 lines)

---

## Task 3: QW-4 - Add Chattering Metrics (2 hours)

### Why Important?
- **Quantitative optimization**: Enables chattering reduction (MT-6 in Week 4)
- **Research contribution**: Measurable chattering index for controller comparison
- **Practical impact**: Chattering reduction = smoother control, less actuator wear

### Current State
- No chattering analysis module exists
- Analysis tools: `src/utils/analysis/statistics.py` (existing)
- Need: FFT analysis, frequency detection, amplitude measurement

### What to Do

**Step 1: Create chattering analysis module** (90 minutes)

**File**: `src/utils/analysis/chattering.py` (~150 lines)

**Implement 4 functions**:

```python
def fft_analysis(control_signal: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Perform FFT analysis on control signal.

    Parameters:
    - control_signal: Control signal u(t), shape (N,)
    - dt: Time step (s)

    Returns:
    - freqs: Frequency array (Hz), shape (N//2,)
    - magnitudes: FFT magnitude spectrum, shape (N//2,)
    """
    # FFT using scipy.fft
    # One-sided spectrum (positive frequencies only)
    # Normalize by N for energy conservation
    pass

def detect_chattering_frequency(
    freqs: np.ndarray,
    magnitudes: np.ndarray,
    threshold_hz: float = 10.0
) -> tuple[float, float]:
    """
    Detect dominant chattering frequency above threshold.

    Parameters:
    - freqs: Frequency array from FFT (Hz)
    - magnitudes: Magnitude spectrum from FFT
    - threshold_hz: Minimum frequency to consider chattering (default 10 Hz)

    Returns:
    - peak_freq: Dominant frequency above threshold (Hz), or 0 if none
    - peak_amplitude: Magnitude at peak frequency
    """
    # Find peak frequency in high-frequency band (> threshold_hz)
    # Return 0 if no significant peak above threshold
    pass

def measure_chattering_amplitude(control_signal: np.ndarray, dt: float) -> float:
    """
    Measure chattering amplitude via control rate RMS.

    Parameters:
    - control_signal: Control signal u(t), shape (N,)
    - dt: Time step (s)

    Returns:
    - chattering_index: RMS of |du/dt| (N/s)
    """
    # Compute du/dt via finite differences
    # Return RMS(|du/dt|) as chattering index
    pass

def compute_chattering_metrics(
    control_signal: np.ndarray,
    dt: float,
    threshold_hz: float = 10.0
) -> dict:
    """
    Compute comprehensive chattering metrics.

    Parameters:
    - control_signal: Control signal u(t), shape (N,)
    - dt: Time step (s)
    - threshold_hz: Chattering frequency threshold (Hz)

    Returns:
    - metrics: Dictionary with keys:
        - 'chattering_frequency': Dominant frequency (Hz)
        - 'chattering_amplitude': Peak magnitude
        - 'chattering_index': RMS(|du/dt|) (N/s)
        - 'total_variation': sum(|du|) (N)
    """
    # Combine all metrics into single dict
    # Add total variation: sum(|u[i+1] - u[i]|)
    pass
```

**Step 2: Add unit tests** (30 minutes)

**File**: `tests/test_utils/test_chattering.py` (~50 lines)

```python
def test_fft_analysis_sine_wave():
    """Test FFT detects known frequency."""
    # Generate 10 Hz sine wave
    # Verify FFT peak at 10 Hz
    pass

def test_detect_chattering_frequency_above_threshold():
    """Test chattering detection above threshold."""
    # Generate signal with 5 Hz + 15 Hz components
    # Verify detects 15 Hz (above 10 Hz threshold)
    pass

def test_chattering_amplitude_measurement():
    """Test RMS chattering amplitude."""
    # Generate signal with known du/dt
    # Verify RMS matches expected value
    pass

def test_compute_chattering_metrics_integration():
    """Test full metrics computation."""
    # Generate realistic control signal
    # Verify all metrics returned
    pass
```

### Expected Output

**New module**: `src/utils/analysis/chattering.py` (~150 lines)
- 4 analysis functions (FFT, frequency detection, amplitude, metrics)
- Comprehensive docstrings with equations
- Type hints (numpy arrays)

**Unit tests**: `tests/test_utils/test_chattering.py` (~50 lines)
- 4 test cases covering all functions
- Known signal validation

**Usage example**:
```python
from src.utils.analysis.chattering import compute_chattering_metrics
import numpy as np

# Load simulation output
u = np.load("simulation_control_output.npy")  # Control signal
dt = 0.01  # Time step

# Analyze chattering
metrics = compute_chattering_metrics(u, dt, threshold_hz=10.0)

print(f"Chattering frequency: {metrics['chattering_frequency']:.2f} Hz")
print(f"Chattering amplitude: {metrics['chattering_amplitude']:.4f}")
print(f"Chattering index: {metrics['chattering_index']:.4f} N/s")
print(f"Total variation: {metrics['total_variation']:.2f} N")
```

### Success Criteria
- [x] Module created with 4 analysis functions
- [x] Unit tests pass (4 test cases)
- [x] Can run on simulation output (u array, dt)
- [x] Returns quantitative chattering metrics
- [x] Ready for MT-6 (Boundary Layer Optimization, Week 4)

### Files Created
- **Create**: src/utils/analysis/chattering.py (~150 lines)
- **Create**: tests/test_utils/test_chattering.py (~50 lines)

---

## Task 4: MT-3 - Adaptive Inertia PSO (3 hours) - HIGHEST ROI

### Why Highest ROI?
- **30% faster convergence**: 50 → 35 generations (15 generation speedup)
- **Low effort**: Modify ~10 lines in existing PSO implementation
- **High impact**: Speeds up ALL future PSO optimization (MT-1, MT-2, MT-5, etc.)
- **Well-tested infrastructure**: 15+ PSO test files validate behavior

### Current State
- PSO implementation: `src/optimization/algorithms/pso_optimizer.py` (905 lines)
- Current inertia: **Fixed w = 0.729** (constant throughout optimization)
- Problem: Slow convergence, poor balance between exploration and exploitation
- Test suite: `tests/test_optimization/` (15+ test files, comprehensive coverage)

### Theory: Time-Varying Inertia Weight

**Problem with fixed inertia**:
- High w (0.9): Good exploration, poor exploitation (slow final convergence)
- Low w (0.4): Poor exploration, good exploitation (premature convergence)
- Fixed w (0.729): Compromise, suboptimal

**Solution: Adaptive inertia**:
- Start high (w = 0.9): Explore search space widely
- End low (w = 0.4): Exploit best regions precisely
- Linear decay: `w(t) = w_max - (w_max - w_min) * t/T`

**Expected gain**: 20-30% faster convergence

### What to Do

**Step 1: Locate inertia weight usage** (15 minutes)
```bash
# Find where inertia is used
grep -n "w_schedule" src/optimization/algorithms/pso_optimizer.py
# Lines 862-894 handle w_schedule (already implemented!)

# Check if adaptive inertia already exists
grep -n "w_values = np.linspace" src/optimization/algorithms/pso_optimizer.py
# Line 866: w_values = np.linspace(float(w_start), float(w_end), iters)
```

**Analysis**: Adaptive inertia **already implemented** via `pso_cfg.w_schedule`!

**Step 2: Verify w_schedule in config** (30 minutes)
```bash
# Check config for w_schedule
grep -n "w_schedule" config.yaml
```

If **w_schedule not in config**, add:
```yaml
pso:
  w: 0.729  # Default inertia (used if w_schedule not set)
  w_schedule:  # NEW: Adaptive inertia
    - 0.9  # w_start (exploration)
    - 0.4  # w_end (exploitation)
  c1: 2.0  # Cognitive coefficient
  c2: 2.0  # Social coefficient
  n_particles: 30
  iters: 100
```

**Step 3: Test adaptive inertia** (90 minutes)

**Test 1: Fixed inertia baseline** (30 min)
```bash
# Run PSO with fixed inertia (w=0.729)
python simulate.py --ctrl classical_smc --run-pso --save week1/results/gains_fixed_inertia.json

# Record:
# - Number of generations to convergence
# - Final best cost
# - Convergence time (wall clock)
```

**Test 2: Adaptive inertia** (30 min)
```bash
# Modify config.yaml: Add w_schedule: [0.9, 0.4]
# Run PSO with adaptive inertia
python simulate.py --ctrl classical_smc --run-pso --save week1/results/gains_adaptive_inertia.json

# Record same metrics
```

**Test 3: Comparison** (30 min)
- Plot convergence curves (best fitness vs generation)
- Compare generations to convergence (expect 35 vs 50, 30% speedup)
- Validate final costs similar (adaptive shouldn't degrade solution quality)

**Step 4: Document results** (45 minutes)
- Save results to `week1/results/pso_adaptive_inertia_comparison.md`
- Include: plots, metrics table, conclusions
- If speedup ≥ 20%, declare success
- If speedup < 20%, document actual gain and adjust expectations

### Expected Output

**Config change**: `config.yaml` (add w_schedule if missing)
```yaml
pso:
  w_schedule: [0.9, 0.4]  # Adaptive inertia (NEW)
```

**Results**:
- Fixed inertia: 50 generations, cost = 0.0245, 120s
- Adaptive inertia: 35 generations, cost = 0.0243, 85s
- **Speedup: 30%** (15 fewer generations, 35s faster)

**Documentation**: `week1/results/pso_adaptive_inertia_comparison.md`
```markdown
# PSO Adaptive Inertia Comparison

## Methodology
- Controller: Classical SMC
- Fixed inertia: w = 0.729
- Adaptive inertia: w(t) from 0.9 → 0.4 linearly
- Trials: 3 runs each (average results)

## Results

| Metric | Fixed (w=0.729) | Adaptive (0.9→0.4) | Improvement |
|--------|-----------------|--------------------| ------------|
| Generations | 50 | 35 | -30% |
| Best cost | 0.0245 | 0.0243 | -0.8% |
| Wall time (s) | 120 | 85 | -29% |

## Conclusion
✅ Adaptive inertia achieves 30% speedup with similar solution quality.
```

### Success Criteria
- [x] w_schedule configured in config.yaml
- [x] Adaptive inertia validated (3 test runs)
- [x] ≥20% convergence speedup achieved (target: 30%)
- [x] Solution quality maintained (final cost within 5% of baseline)
- [x] Results documented with plots

### Files Modified/Created
- **Modify**: config.yaml (add w_schedule if missing)
- **Create**: week1/results/gains_fixed_inertia.json
- **Create**: week1/results/gains_adaptive_inertia.json
- **Create**: week1/results/pso_adaptive_inertia_comparison.md

### Risk Assessment (UPDATED)
- ✅ **LOW RISK**: 15+ test files in tests/test_optimization/ validate PSO behavior
- ✅ **Already implemented**: w_schedule support exists (lines 862-894)
- ✅ **Fallback**: If speedup < 20%, document actual gain, no reversion needed

---

## Task 5: QW-3 - Visualize PSO Convergence (2 hours)

### Why Useful?
- **Visual feedback**: See PSO convergence in real-time plots
- **Debug tool**: Identify premature convergence, stagnation
- **Publication quality**: Convergence plots for research papers

### Current State
- No PSO visualization module
- Visualization utils: `src/utils/visualization/` (static plots, animations exist)
- Need: Convergence plot, particle diversity plot

### What to Do

**Step 1: Create PSO visualization module** (75 minutes)

**File**: `src/utils/visualization/pso_plots.py` (~100 lines)

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_convergence(
    fitness_history: np.ndarray,
    save_path: str = None,
    show: bool = True,
    title: str = "PSO Convergence",
) -> None:
    """
    Plot PSO convergence (best fitness vs generation).

    Parameters:
    - fitness_history: Best fitness per generation, shape (iters,)
    - save_path: Path to save plot (optional)
    - show: Whether to display plot
    - title: Plot title
    """
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, linewidth=2, color='blue')
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Best Fitness (Cost)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale for cost

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()

def plot_diversity(
    position_history: np.ndarray,
    save_path: str = None,
    show: bool = True,
    title: str = "PSO Particle Diversity",
) -> None:
    """
    Plot particle diversity over generations.

    Parameters:
    - position_history: Particle positions, shape (iters, n_particles, n_dims)
    - save_path: Path to save plot
    - show: Whether to display plot
    - title: Plot title
    """
    # Compute diversity as average pairwise distance per generation
    diversity = []
    for gen_positions in position_history:
        # Shape: (n_particles, n_dims)
        # Compute pairwise distances
        dists = np.linalg.norm(
            gen_positions[:, None, :] - gen_positions[None, :, :],
            axis=2
        )
        # Average distance (excluding diagonal)
        avg_dist = np.mean(dists[np.triu_indices_from(dists, k=1)])
        diversity.append(avg_dist)

    plt.figure(figsize=(10, 6))
    plt.plot(diversity, linewidth=2, color='green')
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Particle Diversity (avg pairwise distance)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()

def plot_pso_summary(
    fitness_history: np.ndarray,
    position_history: np.ndarray,
    save_path: str = None,
    show: bool = True,
) -> None:
    """
    Plot PSO summary (convergence + diversity in one figure).

    Parameters:
    - fitness_history: Best fitness per generation
    - position_history: Particle positions history
    - save_path: Path to save plot
    - show: Whether to display plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Convergence plot
    ax1.plot(fitness_history, linewidth=2, color='blue')
    ax1.set_xlabel('Generation', fontsize=12)
    ax1.set_ylabel('Best Fitness (Cost)', fontsize=12)
    ax1.set_title('PSO Convergence', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Diversity plot
    diversity = []
    for gen_positions in position_history:
        dists = np.linalg.norm(
            gen_positions[:, None, :] - gen_positions[None, :, :],
            axis=2
        )
        avg_dist = np.mean(dists[np.triu_indices_from(dists, k=1)])
        diversity.append(avg_dist)

    ax2.plot(diversity, linewidth=2, color='green')
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.set_ylabel('Particle Diversity', fontsize=12)
    ax2.set_title('Particle Diversity Over Time', fontsize=14)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
```

**Step 2: Integrate with simulate.py** (30 minutes)

**Modify simulate.py** to call PSO plots after optimization:

```python
# After PSO optimization completes
if args.run_pso:
    result = tuner.optimise(...)

    # NEW: Generate convergence plots
    from src.utils.visualization.pso_plots import plot_pso_summary

    fitness_history = result['history']['cost']
    position_history = result['history']['pos']

    plot_pso_summary(
        fitness_history=fitness_history,
        position_history=position_history,
        save_path="pso_convergence_summary.png",
        show=True
    )
```

**Step 3: Test visualization** (15 minutes)
```bash
# Run PSO with visualization
python simulate.py --ctrl classical_smc --run-pso --plot

# Verify plots generated:
# - pso_convergence_summary.png (convergence + diversity)
```

### Expected Output

**New module**: `src/utils/visualization/pso_plots.py` (~100 lines)
- 3 plotting functions (convergence, diversity, summary)
- Publication-quality plots (300 DPI, grid, labels)

**Integration**: `simulate.py` (modify PSO section)
- Automatic plot generation after PSO completes

**Example output**:
- **pso_convergence_summary.png**: 2-panel plot showing:
  - Left: Best fitness vs generation (log scale)
  - Right: Particle diversity vs generation
- **Interpretation**:
  - Convergence: Should show monotonic decrease
  - Diversity: Should decrease over time (particles converge)

### Success Criteria
- [x] Module created with 3 plotting functions
- [x] Integration with simulate.py complete
- [x] Plots generated after PSO run
- [x] Publication-quality output (300 DPI, proper labels)
- [x] Visual feedback available for all future PSO optimizations

### Files Created/Modified
- **Create**: src/utils/visualization/pso_plots.py (~100 lines)
- **Modify**: simulate.py (add PSO plot integration)

---

## Daily Schedule

### Day 1: Baseline & Theory (3 hours)

**Morning** (1 hour):
- ☐ Task 1: QW-2 - Run benchmarks (1h)
  - Run pytest benchmarks
  - Generate performance matrix CSV
  - ✅ **Quick win to build momentum!**

**Afternoon** (2 hours):
- ☐ Task 2: QW-1 - Document SMC theory (2h)
  - Read existing theory doc
  - Add formulations for 7 existing controllers
  - Add PLAN sections for 3 future controllers
  - ✅ **Unblocks Week 2 work (MT-1, MT-2)**

**Day 1 Success**: Baseline established + theory documented

---

### Day 2: Metrics & PSO (4 hours)

**Morning** (2 hours):
- ☐ Task 3: QW-4 - Add chattering metrics (2h)
  - Create chattering analysis module (4 functions)
  - Write unit tests (4 test cases)
  - Validate on sample data
  - ✅ **Enables chattering optimization (MT-6 in Week 4)**

**Afternoon** (2 hours, focus time):
- ☐ Task 4: MT-3 - Adaptive inertia PSO (2h baseline, +1h if config changes needed)
  - Check if w_schedule exists in config
  - Add w_schedule if missing
  - Run comparison tests (fixed vs adaptive)
  - Document 30% speedup
  - ✅ **HIGHEST ROI: Speeds up ALL future PSO work**

**Day 2 Success**: Quantitative metrics + 30% faster PSO

---

### Day 3: Visualization & Wrap-up (3 hours)

**Morning** (2 hours):
- ☐ Task 5: QW-3 - Visualize PSO convergence (2h)
  - Create PSO visualization module (3 functions)
  - Integrate with simulate.py
  - Test plot generation
  - ✅ **Visual feedback for optimization debugging**

**Afternoon** (1 hour):
- ☐ Validation & documentation (1h)
  - Run all 5 tasks end-to-end (smoke test)
  - Complete COMPLETION_SUMMARY.md
  - Update DAILY_LOG.md with actuals
  - Verify Week 1 success criteria met

**Day 3 Success**: Week 1 complete, ready for Week 2 (MT-1, MT-2)

---

## Success Criteria

**Week 1 Complete When**:
- [x] All 5 tasks completed (QW-2, QW-1, QW-4, MT-3, QW-3)
- [x] Baseline performance matrix generated (7 controllers × 4 metrics)
- [x] SMC theory documented (+400 lines, 9 controller types)
- [x] Chattering metrics module operational (~150 lines)
- [x] PSO converges 30% faster (35 vs 50 generations)
- [x] Convergence plots generated and integrated
- [x] All deliverables saved to week1/results/
- [x] COMPLETION_SUMMARY.md finalized

**Measurable Outcomes**:
- **Documentation**: +400 lines in docs/theory/smc_theory_complete.md
- **Code**: +250 lines (chattering.py ~150, pso_plots.py ~100)
- **PSO**: 30% faster convergence validated (35 generations vs 50 baseline)
- **Benchmarks**: CSV with 7 controllers × 4 metrics
- **Visualization**: Publication-quality convergence plots

---

## Risk Assessment (CORRECTED)

### Risks Identified

**1. QW-2: Missing controller benchmarks**
- **Risk**: Only 3 controllers benchmarked (Classical, STA, Adaptive), need 7
- **Impact**: Incomplete baseline performance matrix
- **Mitigation**: Document missing controllers (Hybrid, Swing-Up, MPC), defer to Week 2
- **Likelihood**: Medium

**2. QW-1: Theory documentation takes longer than 2h**
- **Risk**: 9 controller formulations might take 3-4 hours (not 2h)
- **Impact**: Day 1 schedule slips
- **Mitigation**: Focus on existing 7 controllers Day 1, defer PLAN sections to Day 2 buffer
- **Likelihood**: Low (existing formulations mostly documented)

**3. MT-3: w_schedule not in config**
- **Risk**: Need to add config section, modify simulate.py integration
- **Impact**: +1 hour overhead (3h → 4h)
- **Mitigation**: w_schedule already implemented (lines 862-894), just add config
- **Likelihood**: Low (implementation exists)

**4. MT-3: Speedup < 30%**
- **Risk**: Adaptive inertia might only achieve 20% speedup (not 30%)
- **Impact**: Lower ROI than expected
- **Mitigation**: Document actual speedup, adjust expectations, still valuable
- **Likelihood**: Low (literature supports 20-30% gains)

**5. Week 1 scope creep**
- **Risk**: User requests additional tasks beyond 5 planned
- **Impact**: Week 1 extends beyond 10 hours
- **Mitigation**: Politely defer to Week 2, stick to plan
- **Likelihood**: Low

### Risk Mitigation Strategies

**Time buffer**: 3 days for 10 hours work = 3.3h/day average (manageable)
**Fallback plans**:
- QW-2: Incomplete benchmarks → document gaps, continue
- QW-1: Theory too long → prioritize existing 7, defer PLAN sections
- MT-3: Config issues → use manual w_schedule in code, defer config.yaml change
- QW-3: Integration issues → standalone script, defer simulate.py integration

---

## Dependencies & Blockers

### Dependencies (Task → Prerequisite)
- **MT-1 (Week 2)** depends on **QW-1 complete** (Terminal SMC theory must be documented)
- **MT-2 (Week 2)** depends on **QW-1 complete** (Integral SMC theory must be documented)
- **MT-6 (Week 4)** depends on **QW-4 complete** (Chattering metrics must exist)
- **All future PSO work** benefits from **MT-3 complete** (Faster convergence)

### Blockers (What Could Stop Week 1?)
- ❌ **None identified** (all tasks self-contained, no external dependencies)
- ✅ **Tests exist**: 15+ PSO test files validate MT-3 changes
- ✅ **Docs exist**: Theory doc ready for updates (QW-1)
- ✅ **Benchmarks exist**: Just need to run + analyze (QW-2)

---

## Files Summary

### Files to Read
- tests/test_benchmarks/core/test_performance.py (QW-2)
- docs/theory/smc_theory_complete.md (QW-1)
- src/optimization/algorithms/pso_optimizer.py (MT-3)
- config.yaml (MT-3)
- simulate.py (QW-3 integration)

### Files to Create (NEW)
- week1/results/baseline_performance.csv (QW-2)
- week1/results/benchmarks.json (QW-2, optional)
- src/utils/analysis/chattering.py (~150 lines, QW-4)
- tests/test_utils/test_chattering.py (~50 lines, QW-4)
- week1/results/gains_fixed_inertia.json (MT-3)
- week1/results/gains_adaptive_inertia.json (MT-3)
- week1/results/pso_adaptive_inertia_comparison.md (MT-3)
- src/utils/visualization/pso_plots.py (~100 lines, QW-3)
- pso_convergence_summary.png (QW-3)

### Files to Modify
- docs/theory/smc_theory_complete.md (+400 lines, QW-1)
- config.yaml (add w_schedule if missing, MT-3)
- simulate.py (PSO plot integration, QW-3)

---

## Next Steps After Week 1

**Week 2-4** (52 hours total):
- **MT-1**: Implement Terminal SMC (10h) - Finite-time convergence
- **MT-2**: Implement Integral SMC (8h) - Disturbance rejection
- **MT-4**: Particle diversity PSO (4h) - Avoid premature convergence
- **MT-5**: Controller performance benchmark (6h) - 9 controllers comparison
- **MT-6**: Boundary layer optimization (5h) - Chattering reduction
- **MT-7**: Reaching time analysis (9h) - Theory validation
- **MT-8**: Disturbance rejection study (7h) - Robustness analysis

**Months 2-3** (97 hours total):
- **LT-1**: Higher-Order SMC (14h) - Academic contribution
- **LT-2**: Hybrid PSO (10h) - 50% faster convergence
- **LT-4**: Lyapunov stability proofs (18h) - Formal verification
- **LT-5**: Multi-objective PSO (15h) - Pareto front analysis
- **LT-7**: Research paper draft (20h) - Publication-ready

---

## Conclusion

Week 1 provides **foundational tools** and **quick wins** that enable all subsequent research work:

1. **QW-2**: Baseline performance → Know where we start
2. **QW-1**: SMC theory → Blueprint for new controllers (MT-1, MT-2)
3. **QW-4**: Chattering metrics → Quantitative optimization (MT-6)
4. **MT-3**: Adaptive PSO → 30% faster for ALL future work
5. **QW-3**: Visualization → Debug tool + publication plots

**Impact**: 10 hours of focused work unlocks 12 weeks of research productivity.

**Start**: Task QW-2 (Run benchmarks) - 1 hour, highest visibility, immediate result.

---

**Files Referenced**:
- tests/test_benchmarks/core/test_performance.py
- docs/theory/smc_theory_complete.md
- src/optimization/algorithms/pso_optimizer.py
- src/utils/analysis/statistics.py
- src/utils/visualization/
- config.yaml
- simulate.py

**Related Documents**:
- .ai/planning/research/ROADMAP.md (12-week research plan)
- .ai/planning/phase3/HANDOFF.md (80-90% research time requirement)
- .ai/planning/phase4/FINAL_ASSESSMENT.md (23.9/100 production score, research-ready)
