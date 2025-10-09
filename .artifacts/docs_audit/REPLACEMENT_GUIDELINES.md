# AI-ish Language Replacement Guidelines

## Principles

1. **Direct, not conversational** - Get to the point immediately
2. **Specific, not generic** - Show concrete features, not abstract claims
3. **Technical, not marketing** - Facts over enthusiasm
4. **Active voice preferred** - Passive acceptable for technical accuracy
5. **Cite, don't hype** - Reference papers instead of using buzzwords

## Pattern Replacements

### Greeting & Conversational Language

| AI-ish Pattern | Professional Alternative | Example Context |
|----------------|-------------------------|-----------------|
| "Let's explore..." | Direct topic sentence | "The simulation runner executes controller logic..." |
| "Let us examine..." | "This section examines..." | "This section examines stability criteria." |
| "We will discuss..." | "This guide covers..." | "This guide covers PSO parameter tuning." |
| "Welcome!" | Remove entirely | Start with content directly |
| "You'll love..." | Remove entirely | Describe features objectively |
| "In this section we will..." | "This section covers..." | "This section covers configuration validation." |
| "Now let's look at..." | "The following demonstrates..." | "The following demonstrates controller integration." |

### Enthusiasm & Marketing Language

| AI-ish Pattern | Professional Alternative | Example Context |
|----------------|-------------------------|-----------------|
| "powerful framework" | "framework" | Let implementation speak for itself |
| "comprehensive solution" | List specific features | "Includes X, Y, Z controllers" |
| "seamless integration" | "integration" | Describe integration, don't hype it |
| "cutting-edge algorithms" | "algorithms" + citation | "PSO optimization (Kennedy & Eberhart, 1995)" |
| "state-of-the-art" | Specific technical claim | "Achieves X performance on Y benchmark" |
| "robust implementation" | Specific reliability features | "Handles edge cases A, B, C" |
| "advanced capabilities" | List actual capabilities | "Supports adaptive gains, nonlinear dynamics" |
| "superior performance" | Quantified comparison | "30% faster convergence vs baseline" |
| "revolutionary approach" | "novel approach" + citation | "Novel hybrid controller (cite paper)" |
| "amazing results" | Quantified results | "RMSE = 0.015, settling time = 2.3s" |

### Hedge Words & Generic Phrases

| AI-ish Pattern | Professional Alternative | Example Context |
|----------------|-------------------------|-----------------|
| "leverage the power of" | "use" | "Use PSO to tune gains" |
| "utilize the optimizer" | "use the optimizer" | "Use the optimizer for parameter search" |
| "delve into the details" | "examine", "analyze" | "Examine the implementation details" |
| "facilitate testing" | "enable testing" OR be specific | "Provides test fixtures for controllers" |
| "employ advanced techniques" | "use" + specify | "Use Lyapunov analysis for stability" |
| "solutions for control" | Be specific | "Controllers: SMC, STA-SMC, adaptive SMC" |
| "capabilities include" | Direct list | "Supports: batch simulation, HIL, PSO" |

### Unnecessary Transitions

| AI-ish Pattern | Professional Alternative | Example Context |
|----------------|-------------------------|-----------------|
| "As we can see" | Remove entirely | "The results show..." (not "As we can see, the results show...") |
| "It's worth noting that" | Remove or integrate | "The system requires..." (not "It's worth noting that the system requires...") |
| "Additionally, it should be mentioned" | "Additionally," OR remove | "Additionally, boundary layer prevents chattering." |
| "Furthermore, we observe that" | "Furthermore," OR "The data shows" | "The data shows convergence in 50 iterations." |
| "Interestingly," | Remove or be specific | "Unexpectedly, the hybrid controller..." |
| "Notably," | Remove or be specific | "The adaptive gain update rate affects..." |

### Repetitive Structures

| AI-ish Pattern | Professional Alternative | Example Context |
|----------------|-------------------------|-----------------|
| "In this section" (repeated) | Vary sentence structure | Use headings instead of repetitive intros |
| "This section covers" (every section) | Direct content | Start with actual information |
| "Let's (explore/examine/look at)" | Imperative or declarative | "Configure the optimizer as follows:" |
| "We (will/can) (see/observe)" | Remove or direct statement | "The controller achieves..." |

## Voice & Tone Standards

### GOOD Examples

**Technical Description:**
```
The PSO optimizer minimizes the cost function using particle swarm dynamics.
Each particle represents a candidate gain set, and the swarm converges to
optimal parameters through velocity updates.
```

**Procedure Documentation:**
```
Controller gains are tuned using the following procedure:

1. Define parameter bounds in config.yaml
2. Run PSO optimization: python simulate.py --run-pso
3. Validate results against acceptance criteria
```

**Stability Claims:**
```
Stability is guaranteed under Lyapunov analysis when sliding surface λ₁s + λ₂ṡ
satisfies conditions in Theorem 3.2 (see Section 3.2).
```

**Performance Results:**
```
The adaptive SMC achieves:
- Settling time: 2.1 ± 0.3 seconds
- RMSE: 0.012 rad
- Control effort: 15.3 N (mean)
```

### BAD Examples (AI-ish)

**Over-enthusiastic Description:**
```
Let's explore the powerful PSO optimizer that seamlessly integrates cutting-edge
particle swarm dynamics! You'll love how it leverages advanced capabilities to
deliver amazing results!
```

**Vague Procedure:**
```
In this comprehensive section, we will delve into the exciting world of controller
tuning. It's worth noting that our robust framework facilitates seamless parameter
optimization through state-of-the-art techniques.
```

**Unsubstantiated Claims:**
```
Our revolutionary stability analysis utilizes advanced Lyapunov techniques to
ensure best-in-class performance with industry-leading reliability.
```

## File-Specific Guidelines

### Getting Started Guides

**Replace:**
- "Welcome! Let's get started with the DIP-SMC-PSO framework!"
- "In this exciting guide, we'll explore the powerful capabilities..."

**With:**
- "This guide covers installation, configuration, and basic simulation."
- "Quick start: Install dependencies → Configure system → Run first simulation"

### Tutorial Files

**Replace:**
- "In this tutorial, we will explore advanced PSO optimization techniques."
- "You'll learn how to leverage the comprehensive testing framework."

**With:**
- "This tutorial demonstrates PSO parameter tuning for adaptive SMC."
- "Learn to configure test suites and validate controller performance."

### API Reference

**Guidelines:**
- Keep technical terminology (even if sounds "robust" in technical context)
- Remove marketing language entirely
- Preserve mathematical rigor
- Use formal parameter descriptions

**Example - Good API Doc:**
```
def compute_control(state, gains, boundary_layer):
    """
    Compute SMC control output.

    Args:
        state: System state [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
        gains: Controller gains [λ₁, λ₂, λ₃, λ₄, K, Φ]
        boundary_layer: Boundary layer thickness (rad)

    Returns:
        Control force (N), bounded by max_force
    ```

### Theory Guides

**Guidelines:**
- Formal academic tone
- Citation-driven claims (no "state-of-the-art" without references)
- Mathematical notation for precision
- Proof-based stability arguments

**Example - Good Theory Doc:**
```
Sliding Mode Control ensures finite-time convergence to the sliding surface
s = λ₁e + λ₂ė = 0 under Assumption 2.1 (bounded disturbances). The control
law u = -(K + Φ)|s| · sgn(s) guarantees reaching condition ṡ · s ≤ -η|s|
for η > 0 (Utkin, 1992).
```

### How-To Guides

**Replace:**
- "Let's learn how to configure the powerful optimization system!"
- "We will utilize advanced techniques to facilitate seamless integration."

**With:**
- "Configure PSO optimization in three steps:"
- "Integration procedure for custom controllers:"

## Technical Terms That Sound AI-ish But Are Acceptable

These terms are acceptable when used in proper technical context:

- **"robust"** - When referring to control theory robustness (H∞, robust stability)
- **"comprehensive"** - When describing complete mathematical coverage
- **"powerful"** - When quantifying computational power (rare, prefer specifics)
- **"advanced"** - When differentiating from basic variants (e.g., "advanced MPC")
- **"enable"** - When describing software flags/options ("enable logging")
- **"facilitate"** - When describing infrastructure ("test fixtures facilitate...")

**Rule:** If it has a precise technical definition, it's acceptable. If it's marketing fluff, remove it.

## Context-Aware Exceptions

### When "Let's" is Acceptable

In interactive tutorial contexts (Jupyter notebooks, live demos):
```
# Interactive Jupyter notebook cell
# Let's run a quick simulation to see the controller response
result = simulate(controller, duration=5.0)
plot(result)
```

This is acceptable because it mirrors natural teaching flow in interactive environments.

### When "Powerful" is Acceptable

When comparing computational resources:
```
PSO optimization requires powerful hardware for large swarm sizes (n > 1000).
Recommended: 8+ CPU cores, 16GB RAM.
```

This is acceptable because "powerful" has quantifiable meaning (CPU cores, RAM).

## Review Checklist

Before finalizing documentation:

- [ ] No greeting language ("Let's", "Welcome")
- [ ] No marketing buzzwords ("seamless", "cutting-edge", "revolutionary")
- [ ] No hedge words ("leverage", "utilize", "delve into")
- [ ] No unnecessary transitions ("As we can see", "It's worth noting")
- [ ] Direct, factual statements
- [ ] Specific examples over generic claims
- [ ] Active voice (except for technical accuracy)
- [ ] Citations for advanced claims
- [ ] Quantified performance claims
- [ ] Technical terms used correctly (not as filler)

## Automation: Pre-Commit Hook (Future)

Planned enhancement: `.git/hooks/pre-commit` script to detect AI patterns before committing docs.

```bash
#!/bin/bash
# Run pattern detection on staged markdown files
python scripts/docs/detect_ai_patterns.py --staged
if [ $? -ne 0 ]; then
    echo "AI-ish patterns detected! Review and fix before committing."
    exit 1
fi
```

---

**Last Updated:** 2025-10-09
**Version:** 1.0
**Maintained By:** Documentation Quality Team
