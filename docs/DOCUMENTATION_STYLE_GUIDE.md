# Documentation Style Guide

**Version:** 1.0
**Last Updated:** 2025-10-09
**Status:** Official Project Standard

---

## Purpose

This guide defines professional writing standards for the DIP-SMC-PSO project documentation based on lessons learned from comprehensive quality audits. Following these standards ensures documentation sounds human-written, professional, and technically accurate.

---

## Core Principles

1. **Direct, not conversational** - Get to the point immediately
2. **Specific, not generic** - Show concrete features, not abstract claims
3. **Technical, not marketing** - Facts over enthusiasm
4. **Show, don't tell** - Concrete examples over buzzwords
5. **Cite, don't hype** - References over marketing language

---

## AI-ish Anti-Patterns (AVOID)

### Greeting & Conversational Language

❌ **DO NOT USE:**
- "Let's explore...", "Let us examine..."
- "Welcome! You'll love..."
- "In this section we will..."
- "Now let's look at..."

✅ **USE INSTEAD:**
- Direct topic sentence: "The PSO optimizer minimizes..."
- "This section covers..."
- "The following demonstrates..."

### Enthusiasm & Marketing Buzzwords

❌ **DO NOT USE:**
- "comprehensive framework" (unless backed by metrics)
- "powerful capabilities"
- "seamless integration"
- "cutting-edge algorithms" (without citations)
- "state-of-the-art" (without citations)
- "robust implementation" (use specific reliability features)

✅ **USE INSTEAD:**
- "framework" (let features speak)
- List specific capabilities
- "integration" (describe, don't hype)
- "PSO optimization (Kennedy & Eberhart, 1995)"
- "Achieves 30% faster convergence vs baseline"
- "Handles edge cases A, B, C"

### Hedge Words

❌ **DO NOT USE:**
- "leverage the power of" → ✅ "use"
- "utilize the optimizer" → ✅ "use the optimizer"
- "delve into the details" → ✅ "examine", "analyze"
- "facilitate testing" → ✅ "enables testing" or be specific

### Unnecessary Transitions

❌ **DO NOT USE:**
- "As we can see..." (redundant)
- "It's worth noting that..." (remove or integrate)
- "Additionally, it should be mentioned..." (verbose)
- "Furthermore, we observe that..." (simplify)

✅ **USE INSTEAD:**
- Remove entirely or state directly
- "The results show..."
- "Additionally," (shorter)
- "The data shows..."

---

## Professional Writing Examples

### GOOD: Technical Description

```
The PSO optimizer minimizes the cost function using particle swarm dynamics.
Each particle represents a candidate gain set, converging to optimal parameters
through velocity updates guided by personal best and global best positions.
```

**Why this works:**
- Direct, factual statements
- Technical terminology used correctly
- No marketing fluff

### BAD: AI-ish Description

```
Let's explore the powerful PSO optimizer with its comprehensive capabilities!
You'll love how seamlessly it leverages cutting-edge particle swarm dynamics
to deliver amazing optimization results through state-of-the-art techniques!
```

**Why this fails:**
- Conversational greeting ("Let's")
- Marketing buzzwords ("powerful", "comprehensive", "seamless", "cutting-edge")
- No specific technical information
- Over-enthusiastic tone

---

### GOOD: Procedure Documentation

```
Controller gains are tuned using the following procedure:

1. Define parameter bounds in config.yaml
2. Run PSO optimization: python simulate.py --run-pso
3. Validate results against acceptance criteria
4. Update config with optimized gains
```

**Why this works:**
- Clear, numbered steps
- Specific commands
- No filler language

### BAD: AI-ish Procedure

```
In this comprehensive section, we will delve into the exciting world of
controller tuning! It's worth noting that our robust framework facilitates
seamless parameter optimization through powerful PSO techniques that leverage
advanced capabilities.
```

**Why this fails:**
- No actual procedural information
- All filler, no content
- Marketing language instead of instructions

---

### GOOD: Performance Claims

```
The adaptive SMC achieves:
- Settling time: 2.1 ± 0.3 seconds
- RMSE: 0.012 rad
- Control effort: 15.3 N (mean)

Performance validated across 10,000 Monte Carlo trials.
```

**Why this works:**
- Quantified metrics
- Statistical confidence intervals
- Validation method specified

### BAD: AI-ish Claims

```
Our revolutionary adaptive SMC delivers amazing performance with industry-leading
settling times and best-in-class accuracy through powerful control algorithms!
```

**Why this fails:**
- No actual numbers
- Unsubstantiated claims
- Marketing superlatives

---

## File-Specific Guidelines

### Getting Started Guides

**Replace:**
- "Welcome! Let's get started with..."
- "You'll love how easy it is to..."

**With:**
- "This guide covers installation and basic usage."
- "Quick start: Install dependencies → Configure → Run simulation"

### Tutorials

**Replace:**
- "In this tutorial, we will explore..."
- "Let's learn how to..."

**With:**
- "This tutorial demonstrates PSO parameter tuning."
- "Learn to configure test suites and validate performance."

### API Reference

**Guidelines:**
- Keep technical terminology (even if it sounds "robust" in context)
- Remove all marketing language
- Preserve mathematical rigor
- Use formal parameter descriptions

**Example:**
```python
def compute_control(state, gains, boundary_layer):
    """
    Compute SMC control output.

    Args:
        state: System state [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
        gains: Controller gains [λ₁, λ₂, λ₃, λ₄, K, Φ]
        boundary_layer: Boundary layer thickness (rad)

    Returns:
        Control force (N), bounded by max_force
    """
```

### Theory Guides

**Guidelines:**
- Formal academic tone
- Citation-driven claims
- Mathematical notation for precision
- Proof-based stability arguments

**Example:**
```
Sliding Mode Control ensures finite-time convergence to the sliding surface
s = λ₁e + λ₂ė = 0 under Assumption 2.1 (bounded disturbances). The control
law u = -(K + Φ)|s| · sgn(s) guarantees reaching condition ṡ · s ≤ -η|s|
for η > 0 (Utkin, 1992).
```

---

## Context-Aware Exceptions

### When Technical Terms Are Acceptable

These terms are acceptable when used in proper technical context:

- **"robust control"** - Formal control theory term (H∞ robustness, μ-synthesis)
- **"comprehensive test coverage: 95%"** - Backed by metrics
- **"enable logging"** - Software configuration terminology
- **"advanced MPC"** - Distinguishing from basic variants

**Rule:** If it has a precise technical definition, it's acceptable. If it's marketing fluff, remove it.

### When "Let's" Is Acceptable

In interactive tutorial contexts (Jupyter notebooks, live demos):

```python
# Interactive Jupyter notebook cell
# Let's run a quick simulation to see the controller response
result = simulate(controller, duration=5.0)
plot(result)
```

This mirrors natural teaching flow in interactive environments.

---

## Pattern Replacement Quick Reference

| AI-ish Pattern | Professional Alternative |
|----------------|-------------------------|
| "Let's explore..." | "The following section covers..." |
| "comprehensive framework" | "framework" (show features) |
| "powerful capabilities" | List specific capabilities |
| "seamless integration" | "integration" |
| "cutting-edge algorithms" | "algorithms" + citation |
| "state-of-the-art" | Specific performance claim + citation |
| "robust implementation" | "Handles edge cases A, B, C" |
| "leverage" | "use" |
| "utilize" | "use" |
| "delve into" | "examine", "analyze" |
| "As we can see" | Remove |
| "It's worth noting that" | Remove or integrate |

---

## Pre-Commit Checklist

Before committing documentation:

- [ ] No greeting language ("Let's", "Welcome")
- [ ] No marketing buzzwords ("seamless", "cutting-edge", "revolutionary")
- [ ] No hedge words ("leverage", "utilize", "delve into")
- [ ] No unnecessary transitions ("As we can see")
- [ ] Direct, factual statements
- [ ] Specific examples over generic claims
- [ ] Active voice (except for technical accuracy)
- [ ] Citations for advanced claims
- [ ] Quantified performance claims
- [ ] Technical terms used correctly (not as filler)

---

## Validation Workflow

1. **Write documentation** using professional standards above
2. **Run pattern detection:**
   ```bash
   python scripts/docs/detect_ai_patterns.py --file path/to/file.md
   ```
3. **Review flagged issues** and apply replacements
4. **Verify technical accuracy** preserved
5. **Commit only when** pattern scan passes (<5 AI-ish patterns detected)

---

## Success Metrics

Documentation must achieve:

- ✅ AI-ish phrase frequency: <10% of October 2025 baseline
- ✅ Tone consistency: 95%+ professional, human-written sound
- ✅ Technical accuracy: Zero regressions
- ✅ Readability: Flesch-Kincaid maintained or improved
- ✅ Peer review standard: "Sounds human-written, professional"

---

## Reference

- **Audit Report:** `.artifacts/docs_audit/AI_PATTERN_AUDIT_REPORT.md`
- **Replacement Guidelines:** `.artifacts/docs_audit/REPLACEMENT_GUIDELINES.md`
- **Pattern Detection Tool:** `scripts/docs/detect_ai_patterns.py`

---

**Maintained By:** Documentation Quality Team
**Questions:** See CLAUDE.md Section 15: Documentation Quality Standards
