# Citation Tracking: Utkin1977 - Variable Structure Systems with Sliding Modes

**Full Citation:**
```bibtex
@article{Utkin1977,
  author = {Vadim I. Utkin},
  title = {Variable Structure Systems with Sliding Modes},
  journal = {IEEE Transactions on Automatic Control},
  volume = {AC-22},
  number = {2},
  pages = {212--222},
  month = {April},
  year = {1977},
  doi = {10.1109/TAC.1977.1101446}
}
```

**Document Info:**
- **Pages:** 212-222 (11 pages)
- **Type:** Survey Paper
- **Publisher:** IEEE
- **File:** `thesis/sources_archive/articles/Utkin1977_Variable_Structure_Systems.pdf`

---

## Document Structure

### Main Sections

1. **Introduction** (p. 212-213)
2. **VSS in Phase Canonic Form** (p. 213-216)
   - Time-Invariant Plants
   - Time-Varying Plants
   - Rejection of Disturbances
3. **Sliding Modes in Discontinuous Dynamic Systems** (p. 217-219)
   - Differential Equations of Sliding Mode
   - Existence of a Sliding Mode
4. **Design of Multiinput VSS** (p. 219-222)

---

## Key Concepts and Definitions

### 1. Variable Structure Systems (VSS)

**Definition** (p. 212):
> "Variable structure systems consist of a set of continuous subsystems together with suitable switching logic. Advantageous properties result from changing structures according to this switching logic."

**LaTeX:**
```latex
\text{VSS: Control switches between structures: } u =
\begin{cases}
u^+(x,t), & \text{if } s(x) > 0 \\
u^-(x,t), & \text{if } s(x) < 0
\end{cases}
```

**Citation:** `\cite[p.~212]{Utkin1977}`

---

### 2. Sliding Mode Phenomenon

**Key Insight** (p. 212):
> "An even more fundamental aspect of VSS is the possibility to obtain trajectories not inherent in any of the structures. These trajectories describe a new type of motion—the so-called sliding mode."

**Sliding Mode Equation** (p. 213):
**LaTeX:**
```latex
\text{For system: } \ddot{x} - \xi\dot{x} + \Psi x = 0
\text{, sliding on } s = cx + \dot{x} = 0 \text{ gives: } \dot{x} + cx = 0
```

**Significance:** Motion dynamics depend only on parameter c, NOT on plant parameters
**Citation:** `\cite[p.~213]{Utkin1977}`

---

### 3. Invariance Property

**Fundamental Result** (Section II, p. 214):

**System:**
```latex
\dot{x}_i = x_{i+1}, \quad i = 1,\ldots,n-1 \\
\dot{x}_n = -\sum_{i=1}^{n} a_i x_i + f(t) + u
```

**Switching Surface:**
```latex
s = \sum_{i=1}^{n} c_i x_i, \quad c_i = \text{const}, \quad c_n = 1
```

**Sliding Mode Equations** (p. 214):
```latex
s = 0 \implies \dot{x}_i = x_{i+1}, \quad i = 1,\ldots,n-2 \\
\dot{x}_{n-1} = -\sum_{i=1}^{n-1} c_i x_i
```

**KEY PROPERTY:** Sliding mode dynamics **independent** of:
- Plant parameters $a_i$
- Disturbance $f(t)$

**Citation:** `\cite[p.~214]{Utkin1977}`

---

### 4. Existence Conditions

**Sufficient Condition for Sliding Mode** (p. 213, Eq. 3):

**LaTeX:**
```latex
\lim_{s \to +0} \dot{s} > 0 \quad \text{and} \quad \lim_{s \to -0} \dot{s} < 0
```

**Interpretation:** Velocity vectors directed toward switching surface from both sides

**Citation:** `\cite[Eq.~3]{Utkin1977}`

---

## Theorems and Key Results

### Theorem 1: Sliding Plane Stability (p. 214)

**Statement:**
> "Let $\lambda_1,\ldots,\lambda_n$ be eigenvalues of the system with $u = \sum_{i=1}^{k} \Omega_i x_i$, where $\Omega_i = c_{i-1} - a_i - c_i c_{n-1} + c_i a_n$. The sliding mode in a sliding plane is asymptotically stable if and only if $\text{Re}\lambda_i < 0$, $i = 1,\ldots,n-1$; one of the eigenvalues is equal to $c_{n-1} - c_n$ and may be arbitrary."

**LaTeX:**
```latex
u = \sum_{i=1}^{k} \Omega_i x_i, \quad \Omega_i = c_{i-1} - a_i - c_i c_{n-1} + c_i a_n
```

**Condition:**
```latex
\text{Asymptotic stability} \iff \text{Re}\lambda_i < 0, \quad i = 1,\ldots,n-1
```

**Citation:** `\cite[Theorem~1, p.~214]{Utkin1977}`

---

### Theorem 2: Truncated System Stability (p. 214)

**Statement:**
> "For the sliding mode in a sliding plane to be asymptotically stable it is sufficient that for the $(n-k+1)$th-order VSS [truncated system], a sliding plane $s' = 0$ with asymptotically stable sliding mode exists."

**Truncated System** (p. 214):
```latex
\dot{x}_i = x_{i+1}, \quad i = k,\ldots,n-1 \\
\dot{x}_n = -\sum_{i=k}^{n} a_i x_i - \sum_{i=1}^{k} \Psi_i^k x_i - \delta_0 \text{sgn}s'
```

**Citation:** `\cite[Theorem~2, p.~214]{Utkin1977}`

---

### Theorem 3: Reaching Condition (p. 215)

**Necessary Condition:**
> "For the state to reach $s = 0$ defined with $c_i > 0$, it is necessary that all real eigenvalues of the systems with $\beta_i = \alpha_i$ be nonnegative."

**Citation:** `\cite[Theorem~3, p.~215]{Utkin1977}`

---

### Theorem 4: Sufficient Reaching Condition (p. 215)

**Statement:**
> "For the state to reach a sliding plane it is sufficient that $c_{n-1} - a_n \leq 0$."

**Citation:** `\cite[Theorem~4, p.~215]{Utkin1977}`

---

### Theorem 6: Combined Condition (p. 215)

**Most Important Result:**
> "The necessary condition of Theorem 3 is also sufficient if the plane $s = 0$ is a sliding plane and the sliding mode is asymptotically stable."

**Design Procedure:**
1. Design sliding mode with desired eigenvalues
2. Ensure existence conditions (Eq. 6)
3. Satisfy reaching conditions by parameter selection

**Citation:** `\cite[Theorem~6, p.~215]{Utkin1977}`

---

## Design Methodology

### Design Procedure for Time-Invariant Plants (p. 214-215)

**Step 1:** Choose desired sliding mode by selecting parameters $c_i$

**Step 2:** Design discontinuous control (p. 214, Eq. 5):
```latex
u = -\sum_{i=1}^{k} \Psi_i x_i - \delta_0 \text{sgn}s, \quad 1 \leq k \leq n-1
```

where
```latex
\Psi_i = \begin{cases}
\alpha_i, & \text{if } x_i s > 0 \\
\beta_i, & \text{if } x_i s < 0
\end{cases}, \quad \text{sgn}s = \begin{cases}
+1, & \text{if } s > 0 \\
-1, & \text{if } s < 0
\end{cases}
```

**Step 3:** Verify existence conditions (p. 214, Eq. 6):
```latex
\alpha_i > c_{i-1} - a_i - c_i c_{n-1} + c_i a_n \\
\beta_i < c_{i-1} - a_i - c_i c_{n-1} + c_i a_n, \quad i = 1,\ldots,k, \quad c_0 = 0 \\
\frac{c_{i-1} - a_i}{c_i} = c_{n-1} - a_n, \quad i = k+1,\ldots,n-1
```

**Step 4:** Ensure reaching conditions

**Citation:** `\cite[pp.~214--215]{Utkin1977}`

---

### Design for Time-Varying Plants (p. 215-216)

**Parameter Ranges:**
```latex
a_i(t) \in [a_{i,\min}, a_{i,\max}], \quad i = 1,\ldots,n
```

**Control Design** (for $k = n-1$):
```latex
\alpha_i \geq \sup_t [c_{i-1} - a_i(t) - c_i c_{n-1} + c_i a_{n-1}(t)] \\
\beta_i \leq \inf_t [c_{i-1} - a_i(t) - c_i c_{n-1} - c_i a_{n-1}(t)], \quad i = 1,\ldots,n-1
```

**KEY ADVANTAGE:** No equality constraints when $k = n-1$, allowing arbitrary $c_i$ selection

**Citation:** `\cite[Eq.~9, p.~215]{Utkin1977}`

---

### Disturbance Rejection (p. 216)

**Problem Setup:**
System with disturbance $f(t) \neq 0$, control must drive $x_1$ (output) to zero along with derivatives.

**Solution:** Augment control with servomechanism (SM):
```latex
u = -\sum_{i=1}^{k} \Psi_k x_i - \delta - \sum_{i=0}^{m-1} \Psi_i^y y^{(i)}
```

**Servomechanism Dynamics** (p. 216, Eq. 12):
```latex
y^{(m)} = -\sum_{i=0}^{m-1} \Psi_i^y y^{(i)} - \delta
```

**Disturbance Class** (p. 216, Eq. 11):
```latex
\left| \frac{d^m f}{dt^m} \right| < B \sum_{i=0}^{m-1} \left| \frac{d^i f}{dt^i} \right|, \quad B = \text{const}
```

**Result:** Zero tracking error for disturbances satisfying (11), including:
- Exponential functions
- Harmonic functions
- Polynomials

**Citation:** `\cite[pp.~216, Eq.~11--12]{Utkin1977}`

---

## Multiinput VSS Design (Section IV, p. 219-222)

### General Form (p. 219)

**System:**
```latex
\dot{x} = Ax + Bu
```

**Switching Surfaces** ($m$ surfaces for $m$ inputs):
```latex
s = Cx, \quad s \in \mathbb{R}^m, \quad C = \text{const}
```

**Control:**
```latex
u_i = \begin{cases}
u_i^+(x,t), & \text{if } s_i(x) > 0 \\
u_i^-(x,t), & \text{if } s_i(x) < 0
\end{cases}, \quad i = 1,\ldots,m
```

**Citation:** `\cite[p.~219]{Utkin1977}`

---

### Design Steps for Multiinput Systems (p. 219)

**Step 1:** Design sliding mode with desired properties (convergence, optimization)

**Step 2:** Ensure existence of sliding manifold at every point of $s = 0$

**Step 3:** Guarantee state reaches sliding manifold

**Citation:** `\cite[p.~219]{Utkin1977}`

---

### Invariance Conditions (p. 220)

**System with Nonlinearities:**
```latex
\dot{x} = Ax + h(x,t) + Bu
```

**Invariance Condition:**
```latex
\text{rank}(B, h) = \text{rank}(B)
```

**Result:** Sliding mode equations independent of $h(x,t)$ if condition satisfied

**Note:** Phase canonic form (Section II) always satisfies this condition

**Citation:** `\cite[Eq.~23, p.~220]{Utkin1977}`

---

## Quick Reference Table

| Concept | Equation/Condition | Page | Citation |
|---------|-------------------|------|----------|
| Sliding surface | $s = \sum c_i x_i = 0$ | 213 | `\cite[p.~213]{Utkin1977}` |
| Existence condition | $\lim_{s \to +0} \dot{s} > 0$ and $\lim_{s \to -0} \dot{s} < 0$ | 213 | `\cite[Eq.~3]{Utkin1977}` |
| Invariance | Dynamics depend only on $c_i$, not $a_i$ or $f(t)$ | 214 | `\cite[p.~214]{Utkin1977}` |
| Control law | $u = -\sum \Psi_i x_i - \delta_0 \text{sgn}s$ | 214 | `\cite[Eq.~5]{Utkin1977}` |
| Stability condition | Re$\lambda_i < 0$, $i = 1,\ldots,n-1$ | 214 | `\cite[Theorem~1]{Utkin1977}` |
| Disturbance class | $\|d^m f/dt^m\| < B \sum \|d^i f/dt^i\|$ | 216 | `\cite[Eq.~11]{Utkin1977}` |

---

## Applications Mentioned

1. **Flight Control** (p. 220, [47], [76])
2. **Chemical Processes** (p. 220, [30])
3. **Industrial Automation** - steel, power, chemical, food industries (p. 220, [33])
4. **Power Stations** (p. 220, [47])

**Citation:** `\cite[p.~220]{Utkin1977}`

---

## Historical Context

**Early Works Referenced** (p. 212):
- Papers from ~20 years before 1977 (mid-1950s)
- References [18], [19], [26], [48], [50], [59], [61], [65], [66], [75], [88], [90]

**Key Innovation:** Combining useful properties of different structures through switching

**Citation:** `\cite[p.~212]{Utkin1977}`

---

## Figures

### Fig. 1 (p. 213):
**Description:** Asymptotically stable VSS from two stable structures
- Shows phase portraits of two stable systems (ellipses)
- Switching on coordinate axes creates asymptotic stability

**Citation:** `\cite[Fig.~1]{Utkin1977}`

### Fig. 2 (p. 213):
**Description:** Asymptotically stable VSS from two unstable structures
- Both structures unstable (spirals outward)
- Switching on specific lines creates stability
- Demonstrates "new properties not present in any structure"

**Citation:** `\cite[Fig.~2]{Utkin1977}`

### Fig. 3 (p. 214):
**Description:** Sliding mode in second-order VSS
- Trajectories converge to switching line $s = cx + \dot{x} = 0$
- Motion along line (sliding mode) governed by $\dot{x} + cx = 0$

**Citation:** `\cite[Fig.~3]{Utkin1977}`

---

## Connection to Thesis Work

### Relevant Sections for DIP-SMC-PSO Project:

1. **Section II** (VSS in Phase Canonic Form):
   - Direct application to inverted pendulum control
   - Design methodology for underactuated systems

2. **Invariance Property** (p. 214):
   - Critical for robust control with parameter uncertainty
   - Justifies PSO optimization focusing on sliding surface parameters $c_i$

3. **Disturbance Rejection** (p. 216):
   - Handling model uncertainties in DIP dynamics
   - External disturbances in swing-up control

4. **Theorem 6** (p. 215):
   - Practical design procedure combining existence and reaching
   - Can guide PSO fitness function design

### How to Cite for Thesis:

**For SMC Background:**
> "Variable structure systems with sliding modes provide robust control through switching between control structures \cite{Utkin1977}. The fundamental property of sliding mode control is invariance to parameter variations and matched disturbances once the system trajectory reaches the sliding surface \cite[p.~214]{Utkin1977}."

**For Existence Conditions:**
> "Following Utkin's sufficient conditions \cite[Eq.~3]{Utkin1977}, a sliding mode exists when trajectories from both sides of the switching surface are directed toward it: $\lim_{s \to +0} \dot{s} > 0$ and $\lim_{s \to -0} \dot{s} < 0$."

**For Design Procedure:**
> "The design of sliding mode controllers for phase-canonic systems follows a systematic procedure \cite[pp.~214--215]{Utkin1977}: (1) design desired sliding mode dynamics by choosing sliding surface parameters, (2) ensure existence conditions, and (3) satisfy reaching conditions."

---

## Notes

- **Original SMC Survey:** This is THE foundational survey paper on sliding mode control
- **Mathematical Rigor:** Provides formal theorems with necessary/sufficient conditions
- **Design Focus:** Emphasis on practical controller synthesis procedures
- **Computational Complexity:** Nondominated sorting is $O(MN^3)$ where referenced
- **Missing:** No explicit discussion of chattering (added in later works)

**Last Updated:** 2025-12-06
