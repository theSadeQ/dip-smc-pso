# E006: Analysis and Visualization Tools

**Part:** Part2 Infrastructure
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Comprehensive Presentation

---

## Overview

This episode covers analysis and visualization tools from the DIP-SMC-PSO project.

## Performance Metrics

**Four Primary Metrics (MT-5 Benchmark):**

        - **Settling Time** -- Time to reach and stay within tolerance
        \begin{equation}
            t_{settle} = \min\{t : \abs{\theta_1(t')}, \abs{\theta_2(t')} < \epsilon \;\forall t' > t\}
        \end{equation}

        - **Overshoot** -- Peak deviation from equilibrium
        \begin{equation}
            \text{Overshoot} = \max_{t} \abs{\theta_1(t)} + \abs{\theta_2(t)}
        \end{equation}

        - **Energy Consumption**
        \begin{equation}
            E = \int_0^T u^2(t) dt
        \end{equation}

        - **Chattering Frequency** -- FFT-based high-frequency content
        \begin{equation}
            E_{HF} = \int_{f > f_{cutoff}} \abs{\mathcal{F}\{u(t)\}}^2 df
        \end{equation}

---

## Statistical Analysis Tools

**Monte Carlo Validation:**

        - **Bootstrap Confidence Intervals** -- 95\
        - **Welch's t-test** -- Compare two controllers (unequal variances)
        - **ANOVA** -- Compare multiple controllers simultaneously
        - **Effect size** -- Cohen's d for practical significance

    **Robustness Ranking (MT-5):**

    \begin{tabular}{lcccc}
        \toprule
        **Controller** & **Mean $t_{settle**$} & **Std Dev** & **95\
        \midrule
        Hybrid Adaptive STA & 2.0 & 0.15 & [1.97, 2.03] & 1 \\
        STA-SMC & 2.1 & 0.18 & [2.06, 2.14] & 2 \\
        Adaptive SMC & 2.3 & 0.22 & [2.26, 2.34] & 3 \\
        Classical SMC & 2.5 & 0.25 & [2.45, 2.55] & 4 \\
        \bottomrule
    \end{tabular**

        All pairwise comparisons: $p < 0.001$ (Welch's t-test)

---

## Publication-Ready Plots

**14 Figures for LT-7 Research Paper:**

        - Control architecture overview
        - Classical SMC boundary layer illustration
        - STA twisting algorithm phase portrait
        - PSO convergence curves (7 controllers)
        - Performance comparison (settling time, overshoot, energy, chattering)
        - Chattering frequency-domain analysis
        - Disturbance rejection time-series (MT-8)
        - Model uncertainty robustness (LT-6)
        - Lyapunov stability regions
        - Monte Carlo statistical validation
        - Controller ranking matrix
        - Comprehensive performance heatmap
        - Energy consumption bar chart
        - Pareto frontier (multi-objective optimization)

        Vector graphics (PDF/EPS), 300 DPI raster, IEEE publication requirements

---



## Visualization Workflow

**Step 1: Generate Simulation Data**
```bash
# Run simulation with plotting enabled
python simulate.py --ctrl classical_smc --plot --save results_classical.json
python simulate.py --ctrl sta_smc --plot --save results_sta.json
python simulate.py --ctrl adaptive_smc --plot --save results_adaptive.json
```

**Step 2: Analyze Performance**
```python
from src.utils.analysis.performance_metrics import calculate_metrics
from src.utils.visualization.plot_comparison import plot_controller_comparison

# Calculate metrics
metrics_classical = calculate_metrics(results_classical)
metrics_sta = calculate_metrics(results_sta)

# Generate comparison plots
plot_controller_comparison([metrics_classical, metrics_sta],
                          labels=['Classical SMC', 'STA-SMC'],
                          output='figures/comparison.pdf')
```

**Step 3: Create Publication Figures**
```bash
# Generate all LT-7 paper figures (14 total)
python scripts/generate_paper_figures.py --task LT-7 --output academic/paper/experiments/figures/
```

---

## Real-Time Monitoring with DIPAnimator

```python
from src.utils.visualization.animator import DIPAnimator

# Create animator
animator = DIPAnimator(dt=0.01, show_traces=True)

# Run simulation with animation
for t in time_steps:
    state = dynamics.step(control, state)
    control = controller.compute_control(state, last_control, history)
    animator.update(state)

# Save animation
animator.save('simulation.mp4', fps=30)
```

**Performance:**
- Real-time 30 FPS rendering
- Trace visualization for trajectory analysis
- Memory usage: 200-500 MB

---

## Statistical Analysis Examples

**Monte Carlo Validation:**
```python
from src.utils.analysis.monte_carlo import run_monte_carlo_analysis

results = run_monte_carlo_analysis(
    controller='classical_smc',
    n_trials=100,
    noise_level=0.1,
    seed=42
)

# Calculate confidence intervals
from src.utils.analysis.statistics import bootstrap_ci
ci_settling = bootstrap_ci(results['settling_time'], confidence=0.95)
print(f"Settling time: {results['settling_time'].mean():.2f} ± {ci_settling[1] - results['settling_time'].mean():.2f}s")
```

**Output:**
```
Settling time: 2.47 ± 0.08s (95% CI: [2.45, 2.55])
Overshoot: 0.15 ± 0.02 rad
Energy: 125.3 ± 8.7 J
Chattering: 12.4 ± 1.8 Hz
```

---

## Chattering Frequency Analysis

```python
from src.utils.analysis.chattering_metrics import analyze_chattering

chattering_data = analyze_chattering(
    control_signal=control_history,
    dt=0.01,
    cutoff_freq=10.0  # Hz
)

# High-frequency energy metric
hf_energy = chattering_data['hf_energy']
print(f"HF energy: {hf_energy:.2f} J")
```

**Boundary Layer Optimization (MT-6):**
- Optimal thickness: δ = 0.05 rad
- Chattering reduction: 60-80%
- Tracking accuracy: ±0.02 rad

---

## Publication Figure Generation

**14 LT-7 Paper Figures:**
1. Architecture overview
2. Boundary layer illustration
3. STA phase portrait
4. PSO convergence (7 controllers)
5-8. Performance comparisons (settling, overshoot, energy, chattering)
9. Disturbance rejection (MT-8)
10. Model uncertainty (LT-6)
11. Lyapunov stability regions
12. Monte Carlo validation
13. Controller ranking matrix
14. Pareto frontier

**Quality Standards:**
- Vector format: PDF/EPS
- Raster fallback: 300 DPI PNG
- Font size: 10-12pt (IEEE two-column)
- File size: <500 KB/figure

---

## Common Pitfalls

**1. Insufficient Monte Carlo Trials**
- Solution: Use n≥100 for adequate statistical power

**2. Ignoring Autocorrelation**
- Solution: Use block bootstrap or subsample

**3. P-hacking Multiple Comparisons**
- Solution: Apply Bonferroni correction (α' = α/n)

**4. Poor Figure Resolution**
- Solution: Always use vector formats (PDF/EPS)

**5. Misleading Y-axis Scales**
- Solution: Start at zero or mark discontinuities clearly

---

## Integration with Research Workflow

**From Simulation to Publication:**
1. Data Collection: Run experiments (MT-5, MT-8, LT-6, LT-7)
2. Statistical Validation: Monte Carlo + bootstrap CI
3. Figure Generation: Automated scripts
4. LaTeX Integration: Include figures with captions
5. Reproducibility: Document seeds, parameters, versions

---

## Performance Benchmarks

- Single figure: 2-5 seconds
- All 14 figures: 45-60 seconds
- Animation: 10-30 seconds/second of video (30 FPS)
- Memory: 100-500 MB depending on task


## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
