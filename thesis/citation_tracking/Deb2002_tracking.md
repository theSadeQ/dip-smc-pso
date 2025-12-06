# Citation Tracking: Deb2002 - A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II

**Full Citation:**
```bibtex
@article{Deb2002,
  author = {Kalyanmoy Deb and Amrit Pratap and Sameer Agarwal and T. Meyarivan},
  title = {A Fast and Elitist Multiobjective Genetic Algorithm: {NSGA-II}},
  journal = {IEEE Transactions on Evolutionary Computation},
  year = {2002},
  volume = {6},
  number = {2},
  pages = {182--197},
  month = {April},
  doi = {10.1109/4235.985692}
}
```

**Document Info:**
- **Pages:** 182-197 (16 pages)
- **Type:** Journal Article
- **Authors:** Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan
- **Institution:** Kanpur Genetic Algorithms Laboratory, Indian Institute of Technology, Kanpur
- **File:** `thesis/sources_archive/articles/Deb2002_NSGA2.pdf`

---

## Document Structure

### Main Sections

1. **Abstract** (p. 182)
2. **Introduction** (pp. 182-183)
3. **Elitist Multiobjective Evolutionary Algorithms** (p. 183)
   - SPEA, PAES, Rudolph's elitist GA
4. **Elitist Nondominated Sorting Genetic Algorithm (NSGA-II)** (pp. 183-186)
   - Fast Nondominated Sorting Approach
   - Diversity Preservation
   - Main Loop
5. **Simulation Results** (pp. 186-192)
   - Test Problems
   - Performance Measures
   - Discussion of Results
   - Different Parameter Settings
6. **Rotated Problems** (pp. 191-192)
7. **Constraint Handling** (pp. 192-195)
   - Proposed Constraint-Handling Approach
   - Ray-Tai-Seow's Approach
   - Simulation Results
8. **Conclusion** (pp. 195-196)
9. **References** (pp. 196-197)

---

## Key Contributions

### Three Main Improvements over NSGA

1. **Reduced Computational Complexity:**
   - Original NSGA: $O(MN^3)$
   - NSGA-II: $O(MN^2)$
   - Fast nondominated sorting procedure

2. **Elitism:**
   - Combines parent and offspring populations
   - Ensures best solutions are never lost
   - Speeds up convergence

3. **Parameter-Less Diversity:**
   - No sharing parameter $\sigma_{\text{share}}$ required
   - Crowding distance mechanism
   - Dynamic and adaptive

**Citation:** `\cite[p.~182]{Deb2002}`

---

## Key Algorithms and Procedures

### 1. Fast Nondominated Sorting

**Complexity:** $O(MN^2)$ where $M$ = objectives, $N$ = population size

**For Each Solution** $p$:
- Calculate domination count $n_p$ (number of solutions dominating $p$)
- Calculate dominated set $S_p$ (solutions dominated by $p$)

**Procedure (p. 184):**
```
For each p in P:
  S_p = empty set
  n_p = 0
  For each q in P:
    if p dominates q:
      Add q to S_p
    else if q dominates p:
      n_p = n_p + 1
  if n_p = 0:
    p belongs to first front F_1

i = 1
while F_i != empty:
  Q = empty
  for each p in F_i:
    for each q in S_p:
      n_q = n_q - 1
      if n_q = 0:
        q belongs to next front
  i = i + 1
  F_i = Q
```

**Citation:** `\cite[p.~184]{Deb2002}`

---

### 2. Crowding Distance Assignment

**Purpose:** Estimate density of solutions surrounding a particular solution

**Procedure (p. 185):**

**LaTeX:**
```latex
i_{\text{distance}} = \sum_{m=1}^{M} \frac{|f_m[i+1] - f_m[i-1]|}{f_m^{\max} - f_m^{\min}}
```

**Algorithm:**
```
l = |I|  (number of solutions in I)
for each i in I: set I[i]_distance = 0
for each objective m:
  I = sort(I, m)
  I[1]_distance = I[l]_distance = infinity
  for i = 2 to (l-1):
    I[i]_distance = I[i]_distance +
                    (I[i+1]_m - I[i-1]_m)/(f_m^max - f_m^min)
```

**Complexity:** $O(MN \log N)$ (dominated by sorting)

**Citation:** `\cite[p.~185]{Deb2002}`

---

### 3. Crowded-Comparison Operator

**Partial Order** $\prec_n$:

**LaTeX:**
```latex
i \prec_n j \text{ if } (i_{\text{rank}} < j_{\text{rank}}) \text{ or }
((i_{\text{rank}} = j_{\text{rank}}) \text{ and } (i_{\text{distance}} > j_{\text{distance}}))
```

**Meaning:**
- Prefer solution with better (lower) nondomination rank
- If same rank, prefer solution in less crowded region

**Citation:** `\cite[p.~185]{Deb2002}`

---

### 4. NSGA-II Main Loop

**Generation** $t$ **Procedure (p. 186):**

```
R_t = P_t ∪ Q_t                 // Combine parent and offspring
F = fast-non-dominated-sort(R_t) // All nondominated fronts
P_{t+1} = empty and i = 1
until |P_{t+1}| + |F_i| <= N:   // Until parent pop is filled
  crowding-distance-assignment(F_i)
  P_{t+1} = P_{t+1} ∪ F_i
  i = i + 1

Sort(F_i, ≺_n)                  // Sort last front by crowded-comparison
P_{t+1} = P_{t+1} ∪ F_i[1 : (N - |P_{t+1}|)]  // Choose first (N - |P_{t+1}|) elements

Q_{t+1} = make-new-pop(P_{t+1}) // Selection, crossover, mutation
t = t + 1
```

**Overall Complexity:** $O(MN^2)$ per generation

**Citation:** `\cite[p.~186]{Deb2002}`

---

## Test Problems

### Problems Used (Table I, p. 187)

1. **SCH** (Schaffer's function): 1 variable, convex
2. **FON** (Fonseca-Fleming): 3 variables, nonconvex
3. **POL** (Poloni): 2 variables, nonconvex, disconnected
4. **KUR** (Kursawe): 3 variables, nonconvex
5. **ZDT1**: 30 variables, convex
6. **ZDT2**: 30 variables, nonconvex
7. **ZDT3**: 30 variables, convex, disconnected
8. **ZDT4**: 10 variables, nonconvex (21^9 local fronts)
9. **ZDT6**: 10 variables, nonconvex, nonuniformly spaced

**Citation:** `\cite[Table~I, p.~187]{Deb2002}`

---

## Performance Metrics

### 1. Convergence Metric $\overline{\Gamma}$

**Definition (p. 188, Fig. 3):**

**LaTeX:**
```latex
\overline{\Gamma} = \frac{\sum_{i=1}^{|Q|} d_i}{|Q|}
```

where:
- $Q$: set of solutions obtained by algorithm
- $d_i$: Euclidean distance of solution $i$ to nearest point in true Pareto-optimal set $P^*$
- $H$: uniformly spaced solutions on $P^*$ (e.g., $H = 500$)

**Interpretation:**
- **Smaller is better**
- Zero when all solutions lie on true Pareto-optimal front
- Measures convergence quality

**Citation:** `\cite[p.~188, Fig.~3]{Deb2002}`

---

### 2. Diversity Metric $\Delta$

**Definition (p. 188, Eq. 1, Fig. 4):**

**LaTeX:**
```latex
\Delta = \frac{d_f + d_l + \sum_{i=1}^{N-1} |d_i - \bar{d}|}{d_f + d_l + (N-1)\bar{d}}
```

where:
- $d_f, d_l$: Euclidean distances between extreme solutions and boundary solutions
- $d_i$: Euclidean distance between consecutive solutions
- $\bar{d}$: average of all $d_i$
- $N$: number of solutions in obtained nondominated set

**Interpretation:**
- **Zero is ideal** (perfect spread and uniformity)
- Larger values indicate worse distribution
- Can be > 1 for highly non-uniform distributions

**Citation:** `\cite[Eq.~1, p.~188]{Deb2002}`

---

## Simulation Results Summary

### Convergence Metric $\overline{\Gamma}$ (Table II, p. 189)

**Mean (Variance) over 10 runs:**

| Algorithm | SCH | FON | POL | KUR | ZDT1 | ZDT2 | ZDT3 | ZDT4 | ZDT6 |
|-----------|-----|-----|-----|-----|------|------|------|------|------|
| NSGA-II (real) | 0.000391 | 0.001931 | 0.015553 | 0.028964 | 0.033482 | 0.072391 | 0.114500 | 0.513053 | 0.296564 |
| NSGA-II (binary) | 0.002833 | 0.002571 | 0.017029 | 0.028951 | 0.000894 | 0.000824 | 0.043411 | 3.220636 | 7.806798 |
| SPEA | 0.003403 | 0.125692 | 0.037812 | 0.045617 | 0.001799 | 0.001339 | 0.047517 | 7.340299 | 0.221138 |
| PAES | 0.001313 | 0.151263 | 0.030864 | 0.057323 | 0.082085 | 0.126276 | 0.023872 | 0.854816 | 0.085469 |

**NSGA-II Wins:** 7/9 problems

**Citation:** `\cite[Table~II, p.~189]{Deb2002}`

---

### Diversity Metric $\Delta$ (Table III, p. 189)

**Mean (Variance) over 10 runs:**

| Algorithm | SCH | FON | POL | KUR | ZDT1 | ZDT2 | ZDT3 | ZDT4 | ZDT6 |
|-----------|-----|-----|-----|-----|------|------|------|------|------|
| NSGA-II (real) | 0.477899 | 0.378065 | 0.452150 | 0.411447 | 0.390307 | 0.430776 | 0.738540 | 0.702612 | 0.668025 |
| NSGA-II (binary) | 0.003471 | 0.000639 | 0.002868 | 0.000992 | 0.001876 | 0.004721 | 0.019706 | 0.066646 | 0.009923 |
| SPEA | 1.021110 | 0.792352 | 0.972783 | 0.852990 | 0.784525 | 0.755148 | 0.672938 | 0.798463 | 0.849389 |
| PAES | 1.063288 | 1.162528 | 1.020007 | 1.079838 | 1.229794 | 1.165942 | 0.789920 | 0.870458 | 1.153052 |

**NSGA-II Wins:** 9/9 problems

**Citation:** `\cite[Table~III, p.~189]{Deb2002}`

---

## Constraint Handling

### Constrained-Domination Definition (p. 192)

**Definition 1:** Solution $i$ constrained-dominates solution $j$ if:

1. Solution $i$ is feasible and $j$ is not, OR
2. Both $i$ and $j$ are infeasible, but $i$ has smaller constraint violation, OR
3. Both $i$ and $j$ are feasible and $i$ dominates $j$

**Properties:**
- Feasible solutions always ranked better than infeasible
- Among infeasible: smaller violation is better
- Among feasible: use standard domination
- **No penalty parameter required**

**Citation:** `\cite[Definition~1, p.~192]{Deb2002}`

---

### Constrained Test Problems (Table V, p. 193)

1. **CONSTR:** 2 variables, 2 objectives, 2 constraints
   - Constrained region is concatenation of constraint boundary + unconstrained Pareto-front

2. **SRN:** 2 variables, 2 objectives, 2 constraints
   - Constrained Pareto-optimal set is subset of unconstrained

3. **TNK:** 2 variables, 2 objectives, 2 constraints
   - Discontinuous Pareto-optimal region on constraint boundary

4. **WATER:** 3 variables, 5 objectives, 7 constraints
   - Five-objective water resource management problem

**Citation:** `\cite[Table~V, p.~193]{Deb2002}`

---

### Constrained NSGA-II vs Ray-Tai-Seow

**Performance on 4 constrained problems:**

- **CONSTR:** NSGA-II finds better spread in both Pareto-optimal regions (Figs. 14-15)
- **SRN:** Both converge well, NSGA-II has better spread (Figs. 16-17)
- **TNK:** NSGA-II finds wide spread on discontinuous front, Ray-Tai-Seow has many infeasible solutions (Figs. 18-19)
- **WATER:** NSGA-II has better spread in most objectives (Table VI, Fig. 21)

**Conclusion:** Constrained NSGA-II outperforms Ray-Tai-Seow's approach

**Citation:** `\cite[Sec.~VI.C, pp.~193--195]{Deb2002}`

---

## Quick Reference Table

| Concept | Equation/Algorithm | Page | Citation |
|---------|-------------------|------|----------|
| Fast nondominated sorting | $O(MN^2)$ complexity | 184 | `\cite[p.~184]{Deb2002}` |
| Crowding distance | $\sum_{m=1}^{M} \frac{\|f_m[i+1] - f_m[i-1]\|}{f_m^{\max} - f_m^{\min}}$ | 185 | `\cite[p.~185]{Deb2002}` |
| Crowded-comparison | $i \prec_n j$ if better rank or less crowded | 185 | `\cite[p.~185]{Deb2002}` |
| Convergence metric | $\overline{\Gamma} = \frac{1}{\|Q\|}\sum d_i$ | 188 | `\cite[p.~188]{Deb2002}` |
| Diversity metric | $\Delta = \frac{d_f + d_l + \sum\|d_i - \bar{d}\|}{d_f + d_l + (N-1)\bar{d}}$ | 188 | `\cite[Eq.~1]{Deb2002}` |
| Constrained-domination | 3-case definition | 192 | `\cite[Def.~1]{Deb2002}` |

---

## Connection to Thesis Work

### Relevance for DIP-SMC-PSO Project:

1. **PSO vs NSGA-II:**
   - Thesis uses PSO for controller tuning
   - NSGA-II is alternative for multiobjective optimization
   - Could be used for Pareto-optimal controller trade-offs

2. **Multiobjective Optimization:**
   - Balance between performance metrics (settling time, overshoot, energy)
   - PSO finds single solution, NSGA-II finds Pareto front
   - Useful for design space exploration

3. **Performance Metrics:**
   - Convergence and diversity metrics applicable to PSO evaluation
   - Could compare PSO with NSGA-II on controller tuning

4. **Constraint Handling:**
   - Constrained NSGA-II approach applicable to PSO
   - Stability constraints, actuator limits
   - Parameter bounds

### How to Cite for Thesis:

**For NSGA-II Background:**
> "NSGA-II \\cite{Deb2002} is a fast elitist multiobjective genetic algorithm with $O(MN^2)$ computational complexity that uses a crowding distance mechanism to maintain diversity without requiring a sharing parameter."

**For Comparison with PSO:**
> "While particle swarm optimization \\cite{Clerc2002} is used in this work for single-objective controller tuning, multiobjective evolutionary algorithms such as NSGA-II \\cite{Deb2002} could be employed to find a Pareto front of controller designs trading off multiple performance objectives."

**For Performance Metrics:**
> "Following Deb et al. \\cite[p.~188]{Deb2002}, we evaluate algorithm performance using convergence and diversity metrics that measure both proximity to the optimal solution and spread of the obtained solution set."

**For Constraint Handling:**
> "We employ a constrained-domination approach \\cite[Def.~1, p.~192]{Deb2002} that ranks feasible solutions better than infeasible ones and compares infeasible solutions based on constraint violation, eliminating the need for penalty parameters."

**For Multiobjective Controller Design:**
> "The controller tuning problem can be formulated as a multiobjective optimization problem \\cite{Deb2002} with objectives including settling time minimization, overshoot minimization, and energy consumption minimization, subject to stability and actuator constraints."

---

## Algorithmic Improvements

### 1. Fast Nondominated Sorting vs Original

**Original NSGA:**
- Complexity: $O(MN^3)$
- Compares each solution with all others, repeatedly

**NSGA-II Fast Sorting:**
- Complexity: $O(MN^2)$
- Uses domination count and dominated set
- Each solution visited at most $N-1$ times

**Speedup:** Factor of $N$ improvement

**Citation:** `\cite[Sec.~III.A, p.~184]{Deb2002}`

---

### 2. Crowding Distance vs Sharing

**Sharing (NSGA):**
- Requires sharing parameter $\sigma_{\text{share}}$
- User must specify or tune
- Complexity: $O(N^2)$ per front

**Crowding Distance (NSGA-II):**
- No user parameter required
- Adaptive to solution distribution
- Complexity: $O(MN \log N)$ (sorting dominates)

**Advantage:** Parameter-less, automatic diversity maintenance

**Citation:** `\cite[Sec.~III.B, pp.~184--185]{Deb2002}`

---

### 3. Elitism Strategy

**Mechanism:**
1. Combine parent $P_t$ and offspring $Q_t$ populations: $R_t = P_t \cup Q_t$ (size $2N$)
2. Sort $R_t$ by nondomination
3. Fill $P_{t+1}$ with best fronts $F_1, F_2, \ldots$ until size $N$ reached
4. Use crowding distance to break ties in last front

**Benefits:**
- Best solutions never lost
- Monotonic improvement in nondominated solutions
- Faster convergence

**Citation:** `\cite[Sec.~III.C, p.~186]{Deb2002}`

---

## Figures

### Fig. 2 (p. 186): NSGA-II Procedure
**Description:** Flowchart showing:
- Combined population $R_t$
- Nondominated sorting to $F_1, F_2, F_3, \ldots$
- Crowding distance sorting of last front
- Rejected solutions
- New parent population $P_{t+1}$

**Citation:** `\cite[Fig.~2]{Deb2002}`

---

### Fig. 3 (p. 188): Distance Metric $\overline{\Gamma}$
**Description:** Illustration of convergence metric calculation
- Pareto-optimal front (curved line)
- Chosen points on front (open circles)
- Obtained solutions (filled circles)
- Euclidean distances $d_i$ shown

**Citation:** `\cite[Fig.~3]{Deb2002}`

---

### Fig. 4 (p. 188): Diversity Metric $\Delta$
**Description:** Illustration of diversity metric components
- Extreme solutions on boundary
- Distances $d_f, d_l$ to boundary
- Consecutive distances $d_1, d_2, \ldots, d_n$

**Citation:** `\cite[Fig.~4]{Deb2002}`

---

### Figs. 5-12 (pp. 189-191): Test Problem Results
**Description:** Nondominated solutions obtained by NSGA-II, PAES, SPEA on:
- SCH (Fig. 5): NSGA-II vs PAES
- KUR (Figs. 6-7): NSGA-II vs SPEA, three disconnected regions
- ZDT2 (Figs. 8-9): NSGA-II vs SPEA, nonconvex front
- ZDT4 (Fig. 10): NSGA-II vs PAES, multimodal (21^9 local fronts)
- ZDT6 (Fig. 11): SPEA vs NSGA-II, nonuniform density

**Citation:** `\cite[Figs.~5--12, pp.~189--191]{Deb2002}`

---

### Fig. 13 (p. 192): Rotated Problem
**Description:** Epistatic problem with rotation matrix
- Decision space and objective space plots
- NSGA-II, PAES, SPEA comparison
- NSGA-II shows best convergence

**Citation:** `\cite[Fig.~13, p.~192]{Deb2002}`

---

### Figs. 14-20 (pp. 194-195): Constrained Problems
**Description:** Results on constrained test problems:
- CONSTR (Figs. 14-15): NSGA-II vs Ray-Tai-Seow
- SRN (Figs. 16-17): Both algorithms
- TNK (Figs. 18-20): NSGA-II, Ray-Tai-Seow, Fonseca-Fleming
- Shows feasible region (shaded) and Pareto-optimal front

**Citation:** `\cite[Figs.~14--20, pp.~194--195]{Deb2002}`

---

### Fig. 21 (p. 196): WATER Problem (5 objectives)
**Description:** Pairwise plots of 5 objectives
- Upper diagonal: NSGA-II results
- Lower diagonal: Ray-Tai-Seow results
- 10 pairwise combinations shown

**Citation:** `\cite[Fig.~21, p.~196]{Deb2002}`

---

## Notes

- **Most Cited MOEA Paper:** NSGA-II is one of the most influential papers in multiobjective optimization
- **Practical Implementation:** Widely used in engineering, operations research, machine learning
- **Open Source:** Many implementations available (MATLAB, Python, C++)
- **Extensions:** Many variants proposed (NSGA-III for many objectives, R-NSGA-II for preferences, etc.)
- **Benchmark Standard:** Used as baseline comparison for new MOEAs
- **Parameter Settings Used:** Population 100, 250-500 generations, SBX crossover ($\eta_c=20$), polynomial mutation ($\eta_m=20$)

**Last Updated:** 2025-12-06
