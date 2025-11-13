# Episode 5: Config Modification - Your First Parameter Experiments

**Duration**: 20-22 minutes | **Learning Time**: 2.5 hours | **Difficulty**: Intermediate

**Part of**: Phase 3.4 - Modifying Configuration (Part 5 of 8)

---

## Opening Hook

Up until now, you've been running simulations with default settings - pendulum masses, lengths, gains, all pre-configured. But what if you want to simulate a DIFFERENT pendulum? Heavier masses? Longer rods? What if you want MORE aggressive control or LESS chattering? Time to open the hood and tweak the engine! In this episode, you'll learn to edit `config dot YAML`, run experiments, and observe how parameters affect performance. Warning: This is addictive. Once you start tweaking, you won't want to stop!

---

## What Is config.yaml?

**YAML** (spelled Y-A-M-L, rhymes with "camel") stands for "YAML Ain't Markup Language" (recursive acronym, very programmer humor). It's a human-readable data format for configuration files.

**Why YAML instead of Python code?** Because users can modify settings WITHOUT understanding Python. You change a number, save the file, run the simulation - no programming needed!

**Location**: In the project root directory:
```
dip-smc-pso/
├── config.yaml  ← THIS FILE!
├── simulate.py
├── src/
└── ...
```

---

## Opening config.yaml

**Windows**:
- Notepad: Right-click `config.yaml` → Open with → Notepad
- VS Code (recommended): Right-click → Open with Code
- Any text editor works!

**Mac/Linux**:
- TextEdit / nano / vim / VS Code

**CRITICAL RULE**: Use SPACES, not TABS for indentation. YAML is whitespace-sensitive. Two spaces per indentation level is standard.

---

## The Structure of config.yaml

Let me give you a tour. Open `config.yaml` and you'll see something like this (simplified):

```yaml
# DIP System Configuration

plant:
  cart_mass: 1.0          # kg
  pendulum1_mass: 0.1     # kg
  pendulum1_length: 0.5   # m
  pendulum2_mass: 0.1     # kg
  pendulum2_length: 0.5   # m
  gravity: 9.81           # m/s²
  friction: 0.01          # damping coefficient

controllers:
  classical_smc:
    gains: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]  # [k1, k2, k3, k4, k5, eta]
    boundary_layer: 0.1

  sta_smc:
    gains: [12.0, 6.0, 10.0, 4.0, 18.0]
    alpha: 0.5

  adaptive_smc:
    gains_initial: [8.0, 4.0, 6.0, 2.0, 12.0, 1.5]
    adaptation_rate: 0.1

  hybrid_adaptive_sta_smc:
    gains_initial: [10.0, 5.0, 8.0, 3.0, 15.0]
    adaptation_rate: 0.1
    alpha: 0.5

simulation:
  duration: 10.0          # seconds
  timestep: 0.01          # seconds (100 Hz)
  initial_disturbance:
    theta1: 0.1           # rad
    theta2: 0.1           # rad

pso:
  num_particles: 30
  num_iterations: 50
  bounds: [[1, 20], [1, 10], [1, 20], [1, 10], [1, 20], [0.5, 5]]
```

**Four Main Sections**:
1. **plant**: Physical parameters of the DIP system
2. **controllers**: Gains for each controller type
3. **simulation**: Time settings and initial conditions
4. **pso**: Optimization settings (we'll use this in Episode 6)

---

## Experiment 1: Heavier Pendulums - The Inertia Challenge

**Hypothesis**: Heavier pendulums are harder to control (more inertia).

**Modification**:

Find the `plant` section:
```yaml
plant:
  pendulum1_mass: 0.1
  pendulum2_mass: 0.1
```

Change to:
```yaml
plant:
  pendulum1_mass: 0.2  # DOUBLED (was 0.1)
  pendulum2_mass: 0.2  # DOUBLED
```

**Save the file** (Ctrl+S or Cmd+S).

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results:
- **Settling time INCREASES**: Maybe from four-point-two to six-point-five seconds
- **Overshoot INCREASES**: From zero-point-zero-three to zero-point-zero-six radians
- **Control effort INCREASES**: From one hundred twenty-five to one hundred eighty Joules
- **Chattering MAY INCREASE**: Controller works harder, more oscillation

**Why?**

Heavier masses have more inertia. Newton's second law: `F equals m times a`. To achieve the same acceleration `a`, you need DOUBLE the force `F` if mass `m` doubles. But our force is LIMITED to plus-or-minus twenty Newtons! So the controller takes longer to stabilize.

**Analogy**: Pushing a shopping cart (light) vs pushing a car (heavy). Same force, different acceleration. Heavier = slower response.

**Restore Defaults**:

After the experiment, change back:
```yaml
plant:
  pendulum1_mass: 0.1  # RESTORED
  pendulum2_mass: 0.1
```

Save the file!

---

## Experiment 2: Longer Pendulums - The Instability Test

**Hypothesis**: Longer pendulums are MORE unstable (fall faster).

**Modification**:

```yaml
plant:
  pendulum1_length: 0.75  # 50% longer (was 0.5)
  pendulum2_length: 0.75
```

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results (DRAMATIC!):
- **Settling time INCREASES**: Maybe from four-point-two to eight-point-zero seconds
- **Overshoot MUCH HIGHER**: Could reach zero-point-one-five radians (nine degrees!)
- **Control effort INCREASES**: One hundred fifty to two hundred Joules
- **System MAY NOT STABILIZE**: With default gains, longer pendulums might diverge!

**Why?**

Longer pendulums have higher gravitational torque. The torque equals `m times g times L times sin-theta`, where `L` is length. Fifty percent longer = fifty percent more torque pulling the pendulum down. The controller must react FASTER and HARDER. Default gains may not be sufficient!

**Analogy**: Balancing a short pencil on your hand (easy) vs balancing a long broomstick (hard). Longer = faster fall, requires quicker reactions.

**If It Doesn't Stabilize**:

You might see:
```
RuntimeError: Simulation diverged (NaN detected)
```

Or plots showing angles growing without bound. This means the controller FAILED - the pendulum fell!

**Solution**: Increase controller gains (next experiment) or reduce length back to defaults.

**Restore Defaults**:

```yaml
plant:
  pendulum1_length: 0.5  # RESTORED
  pendulum2_length: 0.5
```

---

## Experiment 3: Aggressive Gains - Speed vs Smoothness

**Hypothesis**: Higher controller gains = faster settling but more chattering.

**Modification**:

```yaml
controllers:
  classical_smc:
    gains: [20.0, 10.0, 16.0, 6.0, 30.0, 4.0]  # DOUBLED all gains
```

Original gains were `[10.0, 5.0, 8.0, 3.0, 15.0, 2.0]`.

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results:
- **Settling time DECREASES**: Maybe from four-point-two to two-point-eight seconds (FASTER!)
- **Overshoot SLIGHTLY INCREASES**: From zero-point-zero-three to zero-point-zero-four radians
- **Control effort INCREASES**: From one hundred twenty-five to one hundred sixty Joules
- **Chattering MUCH HIGHER**: From zero-point-four-two to zero-point-seven-zero or more!

**Why?**

Higher gains make the controller MORE AGGRESSIVE. It applies larger forces for smaller errors. This speeds convergence BUT increases chatter because small errors cause big force changes.

**Look at Plot 6** (control force):

Default gains:
```
  20|  /\____/\___
   0|_______\___/\__
 -20|
```

Doubled gains:
```
  20| /\/\/\/\___/\/\  ← High-frequency oscillations!
   0|/\/\____\/\____/\
 -20|
```

**Analogy**: Driving with sensitive steering. Gentle steering (low gains) = smooth but slow lane changes. Sensitive steering (high gains) = quick lane changes but jerky, uncomfortable ride.

**Restore Defaults**:

```yaml
controllers:
  classical_smc:
    gains: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]  # RESTORED
```

---

## Experiment 4: Conservative Gains - Smooth but Slow

**Hypothesis**: Lower controller gains = slower settling but smoother control.

**Modification**:

```yaml
controllers:
  classical_smc:
    gains: [5.0, 2.5, 4.0, 1.5, 7.5, 1.0]  # HALVED all gains
```

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results:
- **Settling time INCREASES**: Maybe from four-point-two to eight-point-zero seconds (SLOWER!)
- **Overshoot MAY INCREASE**: System oscillates longer
- **Control effort DECREASES**: From one hundred twenty-five to eighty Joules (more efficient!)
- **Chattering LOWER**: From zero-point-four-two to zero-point-two-five (smoother!)
- **RISK**: System MAY NOT STABILIZE! Too-low gains = insufficient control authority.

**Why?**

Lower gains make the controller LESS AGGRESSIVE. It applies smaller forces, responds more gently. This reduces chattering BUT slows convergence. If gains are TOO low, the pendulums fall faster than the controller can catch them!

**Look at Plot 2** (pendulum one angle):

Default gains: Settles in four seconds.

Halved gains: Oscillates for eight seconds, maybe never fully settles (stays within plus-or-minus zero-point-zero-five radians, never reaches zero-point-zero-one).

**Analogy**: Driving with insensitive steering. You turn the wheel but the car responds slowly. Eventually you get where you're going, but it takes longer and you might overshoot curves!

**Restore Defaults**:

```yaml
controllers:
  classical_smc:
    gains: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]  # RESTORED
```

---

## Experiment 5: Larger Initial Disturbance - Stress Test

**Hypothesis**: Larger disturbances test controller robustness.

**Modification**:

```yaml
simulation:
  initial_disturbance:
    theta1: 0.3  # THREE TIMES larger (was 0.1)
    theta2: 0.3
```

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results:
- **Settling time INCREASES**: Maybe from four-point-two to seven-point-zero seconds
- **Overshoot INCREASES**: From zero-point-zero-three to zero-point-one-zero radians
- **Control effort INCREASES**: From one hundred twenty-five to two hundred Joules
- **Initial response MORE DRAMATIC**: Look at Plots 1-3 - bigger initial movements!

**Why?**

Larger initial disturbance means the pendulums start farther from upright. The controller must work HARDER to bring them back. This is a "stress test" - does the controller handle extreme conditions?

**Real-World Relevance**:

In real systems, disturbances vary. A Segway hits a pothole (large disturbance). A robot arm is bumped (medium disturbance). Testing with large disturbances ensures the controller is ROBUST - works even in worst-case scenarios.

**Restore Defaults**:

```yaml
simulation:
  initial_disturbance:
    theta1: 0.1  # RESTORED
    theta2: 0.1
```

---

## Experiment 6: Reduce Chattering with Boundary Layer

**Hypothesis**: Increasing boundary layer reduces chattering at the cost of slight steady-state error.

**Modification**:

```yaml
controllers:
  classical_smc:
    boundary_layer: 0.5  # INCREASED (was 0.1)
```

**Run Simulation**:
```
python simulate.py --ctrl classical_smc --plot
```

**What Happens**:

Expected results:
- **Settling time SLIGHTLY INCREASES**: From four-point-two to four-point-eight seconds
- **Overshoot SIMILAR**: Minimal change
- **Control effort SLIGHTLY DECREASES**: From one hundred twenty-five to one hundred ten Joules
- **Chattering MUCH LOWER**: From zero-point-four-two to zero-point-two-zero (SMOOTH!)
- **Steady-state error MAY INCREASE**: Final angles might be plus-or-minus zero-point-zero-two instead of zero-point-zero-one (small price for smoothness)

**Why?**

The boundary layer parameter controls the "smoothing" of the SMC sign function. Larger boundary layer = smoother transition from positive to negative force = less chattering. But TOO large = the system doesn't reach exactly zero (small steady-state error).

**Mathematical Detail**:

Classical SMC control law:
```
u equals negative K times tanh of (s divided by epsilon)
```

Where `epsilon` is the boundary layer. Larger epsilon = gentler tanh curve = smoother control.

**Look at Plot 6** (control force):

Small boundary layer (epsilon equals zero-point-one):
```
  20|  /\____/\___   ← Some oscillation
   0|_______\___/\__
 -20|
```

Large boundary layer (epsilon equals zero-point-five):
```
  20|  /~\____       ← Smooth curve!
   0|________\~\___
 -20|
```

**Restore Defaults**:

```yaml
controllers:
  classical_smc:
    boundary_layer: 0.1  # RESTORED
```

---

## CRITICAL: Always Restore Defaults After Experiments!

**Why?** Because subsequent episodes and examples assume default configuration. If you forget to restore, future simulations will behave unexpectedly!

**Quick Restore Method**:

If you're using Git:
```
git checkout config.yaml
```

This reverts `config.yaml` to the last committed version (defaults).

**Manual Restore**:

Keep a backup copy:
```
# Before experiments
cp config.yaml config_backup.yaml

# After experiments
cp config_backup.yaml config.yaml
```

---

## Key Takeaways

**1. YAML is User-Friendly**: Edit numbers, save, run - no programming needed.

**2. Plant Parameters Affect Difficulty**: Heavier = harder, longer = more unstable.

**3. Gains Control Aggressiveness**: Higher = faster + chattery, lower = slower + smooth.

**4. Boundary Layer Reduces Chattering**: At the cost of small steady-state error.

**5. Initial Disturbance Tests Robustness**: Larger disturbances stress-test the controller.

**6. Always Restore Defaults**: After experiments, reset `config.yaml` to avoid confusion.

---

## Pronunciation Guide

- **YAML**: YAM-ul (rhymes with "camel")
- **Inertia**: in-ER-shuh (resistance to acceleration)
- **Torque**: TORK (rotational force)
- **Epsilon**: EP-sih-lon (Greek letter ε, boundary layer parameter)

---

## What's Next

In **Episode 6**, we'll use Particle Swarm Optimization (PSO) to AUTOMATICALLY find optimal gains! No more manual trial-and-error. PSO will run hundreds of simulations, test different gain combinations, and converge on the best values for YOUR weighted cost function. You'll learn:
- How to run PSO optimization (`--run-pso` flag)
- How to customize PSO settings (particle count, iterations)
- How to interpret PSO output
- How to save and load optimized gains

Get ready to automate parameter tuning!

---

**Episode 5 of 8** | Phase 3: Hands-On Learning

**Previous**: [Episode 4 - Performance Metrics](phase3_episode04.md) | **Next**: [Episode 6 - PSO Optimization](phase3_episode06.md)

---

**Usage**: Upload to NotebookLM for podcast discussion of config.yaml modification and parameter experiments.

---

## For NotebookLM: Audio Rendering Notes

**YAML Syntax**: Emphasize indentation rules - "Two spaces, NOT tabs!"

**File Editing**: Walk through finding and opening the file step-by-step

**Experiments**: Use before/after tone - "Before: settling time four-point-two. After: EIGHT-point-zero!"

**Warnings**: Use cautionary tone for "System may not stabilize!" and "Always restore defaults!"

**Plot Descriptions**: Describe control force curves visually (jagged vs smooth)

**Practical Advice**: Emphasize Git restore method and backup strategy - listeners should feel confident experimenting
