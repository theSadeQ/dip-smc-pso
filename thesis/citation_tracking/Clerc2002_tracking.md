# Clerc2002 Citation Tracking
**PDF File**: `clerc2002.pdf`
**BibTeX Key**: `Clerc2002`
**Full Title**: The Particle Swarm—Explosion, Stability, and Convergence in a Multidimensional Complex Space
**Authors**: Maurice Clerc and James Kennedy
**Journal**: IEEE Transactions on Evolutionary Computation
**Year**: 2002
**Volume**: 6, No. 1
**Pages**: 58-73 (document), 16 pages total (PDF)
**DOI**: 10.1109/4235.985692

---

## Document Structure Overview

| Section | Document Pages | PDF Pages | Content Summary |
|---------|---------------|-----------|-----------------|
| Abstract | 58 | 1 | PSO analysis and constriction coefficient introduction |
| 1. Introduction | 58-59 | 1-2 | PSO algorithm description, stochastic explosion problem |
| 2. Algebraic Point of View | 59-61 | 2-4 | Eigenvalue analysis, cyclic behavior, φ < 4 vs φ > 4 |
| 3. Analytic Point of View | 61-65 | 4-8 | Continuous time differential equations, explicit representation |
| 4. Convergence and Space of States | 65-68 | 8-11 | Constriction coefficients, moderate constriction, attractors |
| 5. Generalization | 69 | 12 | Extension to standard two-term PSO formula |
| 6. Running PSO with Constriction | 69-70 | 12-13 | Implementation pseudocode |
| 7. Empirical Results | 70-72 | 13-15 | Benchmark testing on De Jong functions, Schaffer f6, etc. |
| 8. Conclusions | 72-73 | 15-16 | Summary of findings, comparison to evolutionary computation |

---

## Key Theorems and Analytical Results

### Theorem (Implicit - Section 2, p. 60)
**Location**: Page 60, Equation 2.14-2.16
**Statement**: For φ > 4, the distance ||Pt|| from point to center increases like ||L^t Q0||
**Significance**: Proves system explosion when φ > 4
**LaTeX Citation**: `\cite[p.~60, Eq.~2.14]{Clerc2002}`

### Convergence Criterion (Section 4, p. 65)
**Location**: Page 65, Equation 4.1
**Statement**: Convergence occurs when |c'1| < 1 and |c'2| < 1 where c'1, c'2 are eigenvalues
**Significance**: Fundamental condition for PSO convergence
**LaTeX Citation**: `\cite[Eq.~4.1, p.~65]{Clerc2002}`

### Case φ < 4 Analysis (Section 2, p. 60)
**Location**: Pages 59-60
**Statement**: For 0 < φ < 4, eigenvalues are complex and system exhibits cyclic behavior
**Significance**: Explains oscillatory particle behavior
**LaTeX Citation**: `\cite[Sec.~2A, pp.~59--60]{Clerc2002}`

---

## Key Equations and Formulas

### Equation 2.2: Eigenvalues of System Matrix
**Location**: Page 59
**LaTeX**:
```latex
c_1 = 1 - \frac{\varphi}{2} + \frac{\sqrt{\varphi^2 - 4\varphi}}{2}
c_2 = 1 - \frac{\varphi}{2} - \frac{\sqrt{\varphi^2 - 4\varphi}}{2}
```
**Usage**: Fundamental eigenvalue analysis for simplified PSO
**Citation**: `\cite[Eq.~2.2]{Clerc2002}`

### Equation 3.5: General Solution (Analytic View)
**Location**: Page 61
**LaTeX**:
```latex
v(t) = c_1 c_1^t + c_2 c_2^t
```
**Usage**: Continuous-time trajectory solution
**Citation**: `\cite[Eq.~3.5, p.~61]{Clerc2002}`

### Equation 4.3: Type 1 Constriction Coefficient
**Location**: Page 66
**LaTeX**:
```latex
\chi = \frac{\kappa}{|c_2|}, \kappa \in ]0,1[
```
**Usage**: First constriction coefficient formula
**Citation**: `\cite[Eq.~4.3, p.~66]{Clerc2002}`

### Equation 4.15 & 4.17: Canonical Constriction Coefficient (χ)
**Location**: Pages 66-67
**LaTeX**:
```latex
\chi = \frac{2\kappa}{|2 - \varphi - \sqrt{\varphi^2 - 4\varphi}|}, \text{ for } \varphi > 4
```
**Special case (κ=1, φ=4.1)**:
```latex
\chi = \frac{2}{|2 - \varphi - \sqrt{\varphi(\varphi - 4)}|} \approx 0.729
```
**Usage**: **MOST IMPORTANT** - Standard PSO constriction coefficient
**Citation**: `\cite[Eq.~4.15, p.~67]{Clerc2002}` or `\cite[Eq.~4.17]{Clerc2002}`

### Equation 5.3-5.4: Generalized PSO with Constriction
**Location**: Page 69
**LaTeX**:
```latex
v_{id} = \chi \left[ v_{id} + \varphi_1 (p_{id} - x_{id}) + \varphi_2 (p_{gd} - x_{id}) \right]
```
where φ1 and φ2 are random in [0, φmax/2], typically φmax = 4.1
**Usage**: Standard constricted PSO velocity update
**Citation**: `\cite[Eq.~5.3, p.~69]{Clerc2002}`

---

## Figures and Tables

### Figure 1: Cyclic Trajectories
**Location**: Page 60
**Description**: Four subfigures showing cyclic and quasi-cyclic particle trajectories for different φ values (φ=3, φ=(5±√5)/2, φ=2.1)
**Citation**: `\cite[Fig.~1, p.~60]{Clerc2002}`

### Table I: φ Values for Cyclic System
**Location**: Page 60
**Description**: Special φ values yielding cyclic behavior (φ=3, φ=2, φ=(5±√5)/2, φ=1.3, φ=1,2,3,2±√3)
**Citation**: `\cite[Table~I, p.~60]{Clerc2002}`

### Figure 3: Type 1 Constriction Coefficient
**Location**: Page 66
**Description**: Two subfigures showing χ as function of φ and κ
**Citation**: `\cite[Fig.~3, p.~66]{Clerc2002}`

### Figure 4: Discriminant Analysis
**Location**: Page 67
**Description**: Shows discriminant negativity bounds ensuring convergence for different κ values
**Citation**: `\cite[Fig.~4, p.~67]{Clerc2002}`

### Table II: φ Range for Negative Discriminant
**Location**: Page 67
**Description**: Shows φmin and φmax for κ=0.4 and κ=0.99
**Citation**: `\cite[Table~II, p.~67]{Clerc2002}`

### Figure 6: Trajectories with Different φ Values
**Location**: Page 68
**Description**: Six subfigures showing real/imaginary parts of v and y for φ=2.5, φ=3.99, φ=6.0
**Citation**: `\cite[Fig.~6, p.~68]{Clerc2002}`

### Figure 7: Attractor "Trumpet" in 5D Space
**Location**: Page 69
**Description**: Two views of global attractor for φ < 4 case
**Citation**: `\cite[Fig.~7, p.~69]{Clerc2002}`

### Figure 8: Example Trajectory
**Location**: Page 70
**Description**: Trajectory of particle with two φ(p-x) terms
**Citation**: `\cite[Fig.~8, p.~70]{Clerc2002}`

### Table V: Empirical Results
**Location**: Page 72
**Description**: Performance comparison on benchmark functions (f1-f10, Schaffer's f6, Griewank, Ackley, Rastrigin, Rosenbrock)
**Citation**: `\cite[Table~V, p.~72]{Clerc2002}`

---

## Key Sections for Thesis Citation

### Section 1: Introduction (pp. 58-59)
**Content**: PSO algorithm overview, explosion problem due to randomness
**Typical Thesis Usage**: Background on PSO challenges
**Citation Examples**:
```latex
% PSO explosion problem
The particle swarm algorithm exhibits velocity explosion due to
stochastic factors \cite[p.~58]{Clerc2002}, requiring velocity
clamping in traditional implementations.

% Traditional PSO with V_max
Early PSO implementations required an arbitrary V_{max} parameter
to prevent explosion \cite[Sec.~1, p.~59]{Clerc2002}.
```

### Section 2: Algebraic Analysis of Simplified System (pp. 59-61)
**Content**: Eigenvalue analysis, φ < 4 cyclic behavior, φ > 4 explosion
**Typical Thesis Usage**: Theoretical foundation for PSO dynamics
**Citation Examples**:
```latex
% Eigenvalue analysis
The system matrix eigenvalues \cite[Eq.~2.2, p.~59]{Clerc2002}
determine whether the particle exhibits cyclic or explosive behavior.

% Critical value φ = 4
The value φ = 4 is special \cite[p.~59]{Clerc2002}, representing
the boundary between cyclic (φ < 4) and explosive (φ > 4) dynamics.

% Proof of explosion
For φ > 4, ||P_t|| increases like ||L^t Q_0|| \cite[Eq.~2.16, p.~60]{Clerc2002},
proving unbounded particle trajectories.
```

### Section 3: Analytic Point of View (pp. 61-65)
**Content**: Continuous-time differential equations, explicit trajectory representation
**Typical Thesis Usage**: Mathematical analysis of PSO
**Citation Examples**:
```latex
% Continuous time formulation
Assuming continuous time, the PSO dynamics reduce to a classical
second-order differential equation \cite[Eq.~3.2, p.~61]{Clerc2002}.

% General solution
The general solution \cite[Eq.~3.5]{Clerc2002} shows that
v(t) = c_1 c_1^t + c_2 c_2^t, where c_1, c_2 are eigenvalues.
```

### Section 4: Constriction Coefficients (pp. 65-68) **[MOST IMPORTANT]**
**Content**: Introduction of χ (chi) constriction coefficient for guaranteed convergence
**Typical Thesis Usage**: Standard PSO implementation with constriction
**Citation Examples**:
```latex
% Constriction coefficient introduction
Clerc and Kennedy \cite{Clerc2002} introduced the constriction
coefficient χ to ensure PSO convergence without velocity clamping.

% Specific χ value
The canonical constriction coefficient χ ≈ 0.729 \cite[Eq.~4.17]{Clerc2002}
is derived from setting κ = 1 and φ = 4.1.

% Type 1'' constriction formula
The Type 1'' constriction \cite[Eq.~4.15, p.~66]{Clerc2002} is
given by χ = 2κ/|2 - φ - √(φ² - 4φ)| for φ > 4.

% Convergence guarantee
Applying constriction ensures |c'_1| < 1 and |c'_2| < 1
\cite[Eq.~4.1, p.~65]{Clerc2002}, guaranteeing convergence.
```

### Section 5: Generalization to Standard PSO (p. 69)
**Content**: Extension to two-term PSO formula with φ1 and φ2
**Typical Thesis Usage**: Standard PSO implementation
**Citation Examples**:
```latex
% Standard constricted PSO
The generalized constricted PSO \cite[Eq.~5.3, p.~69]{Clerc2002}
updates velocity as v = χ[v + φ_1(p - x) + φ_2(p_g - x)].

% Parameter selection
With φ = φ_1 + φ_2, typically set to 4.1, the constriction
coefficient χ ≈ 0.729 \cite{Clerc2002} ensures convergence.
```

### Section 7: Empirical Results (pp. 70-72)
**Content**: Benchmark testing on De Jong functions, Schaffer f6, Griewank, Rosenbrock
**Typical Thesis Usage**: PSO performance validation
**Citation Examples**:
```latex
% Benchmark performance
Constricted PSO achieved f(x) = 0 on the sphere function (f1)
with 20 particles \cite[Table~V]{Clerc2002}.

% Comparison to genetic algorithms
On Schaffer's f6 function, constricted PSO performed comparably
to genetic algorithms \cite[p.~71]{Clerc2002}.
```

### Section 8: Conclusions (pp. 72-73)
**Content**: Summary of PSO as simple, effective optimizer with biological ties
**Typical Thesis Usage**: PSO overview and motivation
**Citation Examples**:
```latex
% Simplicity of PSO
Particle swarm optimization is an extremely simple algorithm
requiring only primitive mathematical operators \cite[p.~72]{Clerc2002}.

% Comparison to evolutionary computation
PSO has ties to both genetic algorithms (crossover-like adjustment)
and evolutionary programming (stochastic processes) \cite[p.~72]{Clerc2002}.

% Social metaphor
PSO emulates nature by allowing wisdom to emerge rather than
imposing it \cite[p.~73]{Clerc2002}.
```

---

## Quick Reference Table

| Content | Location | Citation | Typical Usage |
|---------|----------|----------|---------------|
| PSO explosion problem | p. 58 | `\cite[p.~58]{Clerc2002}` | Background/motivation |
| Eigenvalues formula | Eq. 2.2, p. 59 | `\cite[Eq.~2.2]{Clerc2002}` | Mathematical analysis |
| φ = 4 critical value | p. 59 | `\cite[p.~59]{Clerc2002}` | Stability boundary |
| Cyclic behavior (φ < 4) | Sec. 2A, pp. 59-60 | `\cite[Sec.~2A, pp.~59--60]{Clerc2002}` | Oscillation explanation |
| Explosion proof (φ > 4) | Eq. 2.16, p. 60 | `\cite[Eq.~2.16, p.~60]{Clerc2002}` | Divergence analysis |
| Continuous time formulation | Eq. 3.2, p. 61 | `\cite[Eq.~3.2, p.~61]{Clerc2002}` | Differential equation |
| Convergence criterion | Eq. 4.1, p. 65 | `\cite[Eq.~4.1, p.~65]{Clerc2002}` | Stability condition |
| **χ (chi) constriction** | **Eq. 4.17, p. 67** | **`\cite[Eq.~4.17]{Clerc2002}`** | **Standard PSO** |
| χ ≈ 0.729 (canonical) | p. 67 | `\cite[p.~67]{Clerc2002}` | Implementation |
| Constricted PSO formula | Eq. 5.3, p. 69 | `\cite[Eq.~5.3, p.~69]{Clerc2002}` | Algorithm |
| Benchmark results | Table V, p. 72 | `\cite[Table~V]{Clerc2002}` | Performance validation |

---

## BibTeX Entry

```bibtex
@article{Clerc2002,
  author  = {Clerc, Maurice and Kennedy, James},
  title   = {The Particle Swarm---Explosion, Stability, and Convergence in a Multidimensional Complex Space},
  journal = {IEEE Transactions on Evolutionary Computation},
  year    = {2002},
  volume  = {6},
  number  = {1},
  pages   = {58--73},
  month   = {February},
  doi     = {10.1109/4235.985692},
  issn    = {1089-778X}
}
```

---

## Citation Statistics
**Times Cited in Thesis**: 0 (update as used)
**Primary Usage**: PSO constriction coefficient, convergence analysis
**Related Work**: Kennedy1995 (original PSO), Eberhart1995 (PSO variants)

---

## Notes
- **Most Important Contribution**: Introduction of χ (chi) constriction coefficient eliminating need for V_max
- **Key Value**: χ ≈ 0.729 with φ = 4.1 is the standard constriction
- **Theoretical Foundation**: Eigenvalue analysis proving convergence conditions
- **Practical Impact**: Enabled PSO to converge without arbitrary parameter tuning
- This paper is one of the most cited PSO papers due to the constriction coefficient

---

**Tracking File Created**: 2025-12-06
**Last Updated**: 2025-12-06
**Status**: ✓ Complete
