# Bibliography & Academic References

Complete academic citations for all control theory, optimization theory, and mathematical foundations used in this project.

## Complete Bibliography

All references organized by category, automatically generated from BibTeX files.

```{bibliography}
:all:
```

---

## References by Category

### Sliding Mode Control Theory

Foundational and advanced SMC techniques including classical, super-twisting, adaptive, and hybrid controllers.

```{bibliography}
:filter: key.startswith("smc_")
```

---

### PSO Optimization Theory

Particle swarm optimization theory, convergence analysis, and parameter tuning methods.

```{bibliography}
:filter: key.startswith("pso_")
```

---

### Stability Theory

Lyapunov stability, finite-time stability, and fixed-time stability analysis.

```{bibliography}
:filter: "khalil" in key or "lyapunov" in key or "bhat" in key or "moulay" in key or "polyakov" in key or "vidyasagar" in key
```

---

### Adaptive Control Theory

Model reference adaptive systems, robust adaptive laws, and parameter estimation.

```{bibliography}
:filter: "astrom" in key or "ioannou" in key or "narendra" in key or "slotine_1986" in key or "plestan" in key or "pomet" in key
```

---

### Fault Detection & Isolation

Threshold selection, hysteresis methods, and robust fault diagnosis techniques.

```{bibliography}
:filter: "gertler" in key or "chen_1999" in key or "isermann" in key or "ding" in key
```

---

### Numerical Methods

Runge-Kutta integration, stiff ODE solvers, and numerical stability analysis.

```{bibliography}
:filter: "press" in key or "hairer" in key or "butcher" in key or "ascher" in key
```

---

### Software & Tools

Python scientific computing libraries and numerical computation frameworks.

```{bibliography}
:filter: key.startswith("soft_") or key.startswith("numpy") or key.startswith("scipy")
```

---

## See Also

For detailed attribution with exact page numbers and theorem references:

- {doc}`../CITATIONS_ACADEMIC` - Academic theory citations linked to exact locations in codebase
- {doc}`../DEPENDENCIES` - Software library citations and licenses
- {doc}`../PATTERNS` - Design pattern attribution and architectural decisions
- {doc}`../CITATIONS` - Master citation index and quick reference guide

---

## Citation Usage in Documentation

To cite a reference in your documentation, use the `{cite}` role:

```markdown
See {cite}`smc_utkin_1992_sliding_modes` for the original sliding mode formulation.

Multiple citations: {cite}`pso_kennedy_1995_particle_swarm_optimization,pso_clerc_2002_particle_swarm`
```

**Example output:**

See {cite}`smc_utkin_1992_sliding_modes` for the original sliding mode formulation.

---

## BibTeX Source Files

The bibliography is generated from the following BibTeX files:

- `refs.bib` - Main bibliography
- `bib/smc.bib` - Sliding mode control references
- `bib/pso.bib` - PSO optimization references
- `bib/stability.bib` - Lyapunov and stability theory
- `bib/adaptive.bib` - Adaptive control theory
- `bib/fdi.bib` - Fault detection and isolation
- `bib/numerical.bib` - Numerical methods and integration
- `bib/software.bib` - Software and tools
- `bib/dip.bib` - Double inverted pendulum references

All BibTeX files are located in the `docs/` and `docs/bib/` directories.
