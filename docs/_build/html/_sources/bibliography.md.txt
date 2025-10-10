# Bibliography & Academic References

Complete academic citations for all control theory, optimization theory, and mathematical foundations used in this project.

## Complete Bibliography

All references organized by category, automatically generated from BibTeX files.

<!-- Complete bibliography section removed to prevent duplicate citations.
     All citations are shown in their respective categories below. -->

## References by Category

### Sliding Mode Control Theory

Foundational and advanced SMC techniques including classical, super-twisting, adaptive, and hybrid controllers.

```{bibliography}
:filter: key % "smc_"
```



### PSO Optimization Theory

Particle swarm optimization theory, convergence analysis, and parameter tuning methods.

```{bibliography}
:filter: key % "pso_"
```



### Stability Theory

Lyapunov stability, finite-time stability, and fixed-time stability analysis.

```{bibliography}
:filter: key % "khalil" or key % "lyapunov" or key % "bhat" or key % "moulay" or key % "polyakov" or key % "vidyasagar"
```



### Adaptive Control Theory

Model reference adaptive systems, robust adaptive laws, and parameter estimation.

```{bibliography}
:filter: key % "astrom" or key % "ioannou" or key % "narendra" or key % "slotine_1986" or key % "plestan" or key % "pomet"
```



### Fault Detection & Isolation

Threshold selection, hysteresis methods, and robust fault diagnosis techniques.

```{bibliography}
:filter: key % "gertler" or key % "chen_1999" or key % "isermann" or key % "ding"
```



### Numerical Methods

Runge-Kutta integration, stiff ODE solvers, and numerical stability analysis.

```{bibliography}
:filter: key % "press" or key % "hairer" or key % "butcher" or key % "ascher"
```



### Software & Tools

Python scientific computing libraries and numerical computation frameworks.

```{bibliography}
:filter: key % "soft_" or key % "numpy" or key % "scipy"
```



## See Also

For detailed attribution with exact page numbers and theorem references:

- {doc}`../CITATIONS_ACADEMIC` - Academic theory citations linked to exact locations in codebase
- {doc}`../DEPENDENCIES` - Software library citations and licenses
- {doc}`../PATTERNS` - Design pattern attribution and architectural decisions
- {doc}`../CITATIONS` - Master citation index and quick reference guide



## Citation Usage in Documentation

To cite a reference in your documentation, use the `{cite}` role:

```markdown
See {cite}`smc_utkin_1992_sliding_modes` for the original sliding mode formulation.

Multiple citations: {cite}`pso_kennedy_1995_particle_swarm_optimization,pso_clerc_2002_particle_swarm`
```

**Example output:**

See {cite}`smc_utkin_1992_sliding_modes` for the original sliding mode formulation.



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
