# Episode 6: PSO Optimization - Let the Swarm Find Optimal Gains

**Duration**: 16-18 minutes | **Learning Time**: 2 hours | **Difficulty**: Intermediate

**Part of**: Phase 3.4 - Parameter Tuning with PSO (Part 6 of 8)

---

## Opening Hook

In Episode 5, you manually tweaked gains - doubling them, halving them, observing effects. But finding OPTIMAL gains by hand is like searching for a needle in a six-dimensional haystack. There are six gains, each with twenty possible values - that's sixty-four MILLION combinations! Manual tuning would take thirty years. Enter Particle Swarm Optimization: thirty intelligent agents exploring the parameter space simultaneously, converging on the best gains in ten to twenty minutes. In this episode, you'll run PSO, watch it optimize, and load the optimized gains for a final simulation. Let the swarm do the work!

---

## Recap: What Is PSO?

**Quick Refresher** (details in Phase 2, Episode 9):

Particle Swarm Optimization is a bio-inspired algorithm that mimics bird flocking or fish schooling. Key ideas:
- **Swarm**: Thirty "particles" (candidate gain sets)
- **Exploration**: Each particle tries different gains
- **Communication**: Particles share information ("I found good gains here!")
- **Convergence**: Over fifty iterations, the swarm converges on optimal gains

**What PSO Optimizes**:

A weighted cost function:
```
J equals w1 times settling-time plus w2 times overshoot plus w3 times control-effort plus w4 times chattering
```

Lower `J` = better performance. PSO finds gains that MINIMIZE `J`.

---

## Running PSO: The Simplest Command

**The Command**:

```
python simulate.py --ctrl classical_smc --run-pso --save optimal_gains.json
```

Phonetically:
- `python simulate dot p-y space dash dash ctrl classical underscore s-m-c`
- `space dash dash run hyphen p-s-o`
- `space dash dash save optimal underscore gains dot json`

**What Happens**:

1. PSO initializes thirty particles with random gains
2. For each particle, runs a simulation and calculates cost `J`
3. Updates particle positions (new gains) based on swarm intelligence
4. Repeats for fifty iterations (thirty particles times fifty = one thousand five hundred simulations total!)
5. Converges on optimal gains
6. Saves result to `optimal underscore gains dot json`

**Duration**: Ten to twenty minutes (depends on your computer speed).

---

## Console Output: What You'll See

**Initialization Phase**:

```
[INFO] Starting PSO optimization...
[INFO] Controller: Classical SMC
[INFO] Swarm size: 30 particles
[INFO] Iterations: 50
[INFO] Cost function: weighted (settling=2.0, overshoot=5.0, effort=0.1, chatter=3.0)

Initializing particles... [OK]
```

**Iteration Progress**:

```
Iteration 1/50:
  Best cost: 45.3
  Best gains: [8.2, 4.1, 9.7, 3.5, 14.2, 1.8]
  Time: 12.4 seconds

Iteration 10/50:
  Best cost: 28.7
  Best gains: [11.5, 5.8, 10.2, 4.3, 16.8, 2.4]
  Time: 118.3 seconds

Iteration 20/50:
  Best cost: 18.2
  Best gains: [12.3, 6.1, 11.1, 4.7, 18.2, 2.7]
  Time: 235.1 seconds

Iteration 30/50:
  Best cost: 12.5
  Best gains: [12.7, 7.2, 11.5, 5.1, 19.0, 2.9]
  Time: 351.8 seconds

Iteration 40/50:
  Best cost: 10.8
  Best gains: [12.9, 7.5, 11.8, 5.3, 19.3, 3.0]
  Time: 468.5 seconds

Iteration 50/50:
  Best cost: 10.3
  Best gains: [12.95, 7.58, 11.92, 5.42, 19.45, 3.05]
  Time: 585.2 seconds (9.75 minutes)
```

**Final Output**:

```
[INFO] PSO optimization complete!
[INFO] Final optimized gains: [12.95, 7.58, 11.92, 5.42, 19.45, 3.05]
[INFO] Final cost: 10.3
[INFO] Performance metrics with optimized gains:
  - Settling time: 3.1 seconds
  - Max overshoot: 0.018 rad (1.0 degrees)
  - Control effort: 98.5 J
  - Chattering index: 0.28

[INFO] Gains saved to: optimal_gains.json
[OK] PSO complete in 9.75 minutes.
```

**Key Observations**:

- **Cost decreases**: From forty-five-point-three (iteration 1) to ten-point-three (iteration 50)
- **Gains evolve**: Early guesses are random, later iterations fine-tune
- **Convergence**: Around iteration thirty, cost improvements slow (swarm is converging)
- **Time**: Nine-point-seven-five minutes total for one thousand five hundred simulations

---

## Understanding the Optimized Gains

**Original Default Gains**:
```
[10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
```

**PSO-Optimized Gains**:
```
[12.95, 7.58, 11.92, 5.42, 19.45, 3.05]
```

**Comparison**:

| Gain | Default | Optimized | Change |
|------|---------|-----------|--------|
| k1 | 10.0 | 12.95 | +29% |
| k2 | 5.0 | 7.58 | +52% |
| k3 | 8.0 | 11.92 | +49% |
| k4 | 3.0 | 5.42 | +81% |
| k5 | 15.0 | 19.45 | +30% |
| eta | 2.0 | 3.05 | +53% |

**Interpretation**:

PSO increased ALL gains! Why? Because the cost function weights fast settling (w1 equals two-point-zero) and low overshoot (w2 equals five-point-zero). Higher gains achieve this, at the cost of slightly higher chattering (but chattering weight w4 equals three-point-zero is moderate, so PSO tolerates it).

**Different Weights = Different Optimal Gains**:

If you prioritize energy efficiency (increase w3), PSO would find LOWER gains. If you prioritize smoothness (increase w4), PSO would reduce chattering at the expense of speed.

---

## Loading and Using Optimized Gains

**The JSON File**:

After PSO completes, open `optimal underscore gains dot json`:

```json
{
  "controller": "classical_smc",
  "gains": [12.95, 7.58, 11.92, 5.42, 19.45, 3.05],
  "cost": 10.3,
  "metrics": {
    "settling_time": 3.1,
    "overshoot": 0.018,
    "control_effort": 98.5,
    "chattering_index": 0.28
  },
  "pso_iterations": 50,
  "timestamp": "2025-11-13T10:30:45"
}
```

**Loading Gains for Simulation**:

```
python simulate.py --ctrl classical_smc --load optimal_gains.json --plot
```

Phonetically:
- `dash dash load optimal underscore gains dot json`

**What Happens**:

Instead of using default gains from `config.yaml`, the script loads gains from `optimal underscore gains dot json` and runs a simulation with them.

**Compare to Default**:

Run both:
```
python simulate.py --ctrl classical_smc --plot --save default_results.json
python simulate.py --ctrl classical_smc --load optimal_gains.json --plot --save optimized_results.json
```

**Expected Improvements**:

| Metric | Default | Optimized |
|--------|---------|-----------|
| Settling Time | 4.2 s | 3.1 s (26% faster!) |
| Overshoot | 0.03 rad | 0.018 rad (40% less!) |
| Control Effort | 125 J | 98.5 J (21% more efficient!) |
| Chattering | 0.42 | 0.28 (33% smoother!) |

**It's BETTER on ALL metrics!** That's the power of PSO - multi-objective optimization!

---

## Customizing PSO Settings

**Default PSO Settings** (from `config.yaml`):

```yaml
pso:
  num_particles: 30
  num_iterations: 50
  bounds: [[1, 20], [1, 10], [1, 20], [1, 10], [1, 20], [0.5, 5]]
```

**What These Mean**:

- **num_particles**: Swarm size (thirty particles)
- **num_iterations**: How many generations (fifty)
- **bounds**: Min/max values for each gain
  - k1: between one and twenty
  - k2: between one and ten
  - k3: between one and twenty
  - k4: between one and ten
  - k5: between one and twenty
  - eta: between zero-point-five and five

**Customizing**:

Open `config.yaml`, modify the `pso` section:

**Faster optimization** (fewer particles/iterations):
```yaml
pso:
  num_particles: 20
  num_iterations: 30
```

Result: Runs in five minutes instead of ten, but may find suboptimal gains.

**More thorough optimization**:
```yaml
pso:
  num_particles: 50
  num_iterations: 100
```

Result: Runs in forty minutes, finds better gains.

**Tighter bounds** (if you know gains should be near defaults):
```yaml
pso:
  bounds: [[8, 15], [3, 8], [6, 12], [2, 6], [12, 20], [1.5, 4]]
```

Result: Faster convergence, but PSO won't explore outside these ranges.

---

## PSO for Other Controllers

**Optimize STA-SMC**:

```
python simulate.py --ctrl sta_smc --run-pso --save optimal_sta_gains.json
```

**Optimize Adaptive SMC**:

```
python simulate.py --ctrl adaptive_smc --run-pso --save optimal_adaptive_gains.json
```

**Optimize Hybrid**:

```
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --save optimal_hybrid_gains.json
```

Each controller has a different gain structure, so PSO adapts to find optimal parameters for THAT specific controller!

---

## Troubleshooting PSO

**Issue 1: PSO Takes Too Long**

**Solution**: Reduce particles or iterations:
```yaml
pso:
  num_particles: 20
  num_iterations: 30
```

Or use a faster controller (Classical is fastest to simulate).

---

**Issue 2: PSO Finds "Bad" Gains (System Doesn't Stabilize)**

**Cause**: Cost function weights may prioritize wrong objectives, or bounds are too wide.

**Solution 1**: Tighten bounds to reasonable ranges.

**Solution 2**: Adjust cost function weights (requires modifying Python code - advanced!).

**Solution 3**: Use default gains as starting point.

---

**Issue 3: PSO Gets Stuck (Cost Plateaus Early)**

**Cause**: Premature convergence - swarm lost diversity.

**Solution**: Increase particle count or use wider bounds.

---

## Key Takeaways

**1. PSO Automates Tuning**: No more manual trial-and-error - PSO finds optimal gains in minutes.

**2. Swarm Intelligence**: Thirty particles explore, communicate, converge on best solution.

**3. Multi-Objective Optimization**: PSO minimizes weighted cost function (speed, precision, efficiency, smoothness).

**4. Customizable**: Adjust particles, iterations, bounds in `config.yaml`.

**5. Controller-Specific**: Run PSO for each controller type to find its optimal gains.

**6. Load and Compare**: Use `--load` flag to run simulations with optimized gains.

---

## Pronunciation Guide

- **PSO**: P-S-O (Particle Swarm Optimization)
- **JSON**: JAY-sawn (JavaScript Object Notation)
- **Iteration**: ih-tuh-RAY-shun (one generation of the swarm)
- **Convergence**: kun-VER-junce (approaching optimal solution)

---

## What's Next

In **Episode 7**, we'll tackle troubleshooting:
- Common errors and how to fix them
- What to do when simulations fail
- Debugging YAML syntax errors
- Handling ModuleNotFoundError, RuntimeError, etc.
- Getting help when stuck

You'll become a confident problem-solver!

---

**Episode 6 of 8** | Phase 3: Hands-On Learning

**Previous**: [Episode 5 - Config Modification](phase3_episode05.md) | **Next**: [Episode 7 - Troubleshooting Guide](phase3_episode07.md)

---

**Usage**: Upload to NotebookLM for podcast discussion of PSO optimization workflow and automated parameter tuning.

---

## For NotebookLM: Audio Rendering Notes

**Console Output**: Use robotic/monotone voice for console messages to distinguish from narration

**Numbers**: Emphasize decreasing cost over iterations - "Forty-five-point-three... DOWN to twenty-eight-point-seven... DOWN to eighteen-point-two..."

**Timings**: Give listeners sense of duration - "Nine-point-seven-five minutes total - time for a coffee break!"

**Comparisons**: Use before/after tone - "Default: four-point-two seconds. Optimized: THREE-point-one! Twenty-six percent faster!"

**Troubleshooting**: Use helpful, patient tone - "Don't worry, this is fixable..."

**Encouragement**: End with motivational message - "PSO just saved you HOURS of manual tuning!"
