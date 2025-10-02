# Common Citations Database

**Purpose:** Quick reference for frequently-used citations across multiple research batches

**How to use:**
1. When you find a citation that appears in multiple batches, add it here
2. Use this database to quickly fill similar claims without re-researching
3. Copy BibTeX entries for reference management

**Citation Reuse Efficiency:** High reuse rate = faster research!

---

## Sliding Mode Control (Classical)

### Utkin (1977) - *Variable Structure Systems with Sliding Modes*

- **BibTeX Key:** `utkin1977variable`
- **Type:** journal
- **DOI:** 10.1109/TAC.1977.1101446
- **Journal:** IEEE Transactions on Automatic Control, Vol. AC-22, No. 2, pp. 212-222
- **Citations:** 5,220+ (seminal paper - THE foundational SMC reference)
- **Used in batches:**
  - Batch 06 (Claim 1): CRITICAL - Super-Twisting SMC (classical SMC finite-time convergence)

**Key topics covered:**
- Seminal formulation of variable structure systems
- Classical sliding mode control law: $\dot{s} = -\eta \, \mathrm{sign}(s)$
- Reaching condition: $s \dot{s} = -\eta |s|$ for finite-time convergence
- Matched uncertainty compensation
- Global finite-time convergence to sliding surface

**When to use:**
- THE foundational citation for classical SMC theory
- Finite-time convergence proofs for SMC
- Switching gain design to exceed disturbance bounds
- Variable structure systems theory

**BibTeX Entry:**
```bibtex
@article{utkin1977variable,
  title={Variable Structure Systems with Sliding Modes},
  author={Utkin, Vadim I.},
  journal={IEEE Transactions on Automatic Control},
  volume={22},
  number={2},
  pages={212--222},
  year={1977},
  publisher={IEEE},
  doi={10.1109/TAC.1977.1101446}
}
```

---

### Slotine & Li (1991) - *Applied Nonlinear Control*

- **BibTeX Key:** `slotine1991applied`
- **Type:** book
- **DOI:** N/A
- **Accessible URL:** https://vtechworks.lib.vt.edu/bitstream/handle/10919/30598/CHAP4_DOC.pdf
- **Publisher:** Prentice Hall
- **Used in batches:**
  - Batch 01 (Claims 2, 4): Sliding Mode Classical
  - Batch 11 (expected): HIGH - Sliding Mode Classical

**Key topics covered:**
- Chapter 5: Sliding Mode Control
  - Reaching conditions and finite-time convergence (Section 5.2)
  - Boundary layer method for chattering reduction (Section 5.4)
  - Lyapunov stability analysis (Section 5.3)

**When to use:**
- Classical SMC reaching time bounds
- Boundary layer / chattering reduction claims
- Sliding surface design and stability

**BibTeX Entry:**
```bibtex
@book{slotine1991applied,
  title={Applied Nonlinear Control},
  author={Slotine, Jean-Jacques E and Li, Weiping},
  year={1991},
  publisher={Prentice Hall},
  address={Englewood Cliffs, NJ},
  isbn={0-13-040890-5}
}
```

---

### Utkin (1992) - *Sliding Modes in Control and Optimization*

- **BibTeX Key:** `utkin1992sliding`
- **Type:** book
- **DOI:** 10.1007/978-3-642-84379-2
- **Publisher:** Springer-Verlag
- **Used in batches:**
  - Batch 01 (expected if needed)
  - Batch 05 (Claim 2): CRITICAL - Inverted Pendulum (SMC Lyapunov stability)
  - Batch 11 (expected)

**Key topics covered:**
- Variable structure systems theory
- Discontinuous control fundamentals
- Chattering phenomenon analysis

**When to use:**
- Theoretical foundations of SMC
- Variable structure systems
- Original SMC formulations

---

### Edwards & Spurgeon (1998) - *Sliding Mode Control: Theory and Applications*

- **BibTeX Key:** `edwards1998sliding`
- **Type:** book
- **DOI:** 10.1201/9781498701822
- **Publisher:** CRC Press

**When to use:**
- Modern SMC formulations
- Robust control applications
- Output feedback SMC

---

## Sliding Mode Control (Super-Twisting)

### Levant (2003) - *Higher-order sliding modes, differentiation and output-feedback control*

- **BibTeX Key:** `levant2003higher`
- **Type:** journal
- **DOI:** 10.1080/0020717031000099029
- **Journal:** International Journal of Control, 76(9-10), 924-941
- **Used in batches:**
  - Batch 06 (expected): CRITICAL - Super-Twisting
  - Batch 14 (expected): HIGH - Super-Twisting

**Key topics covered:**
- Super-Twisting Algorithm (STA)
- Higher-order sliding modes
- Finite-time convergence proofs
- 2nd order sliding mode design

**When to use:**
- Super-twisting / 2-SMC claims
- Finite-time convergence for STA
- Chattering-free continuous control

**BibTeX Entry:**
```bibtex
@article{levant2003higher,
  title={Higher-order sliding modes, differentiation and output-feedback control},
  author={Levant, Arie},
  journal={International Journal of Control},
  volume={76},
  number={9-10},
  pages={924--941},
  year={2003},
  publisher={Taylor \& Francis},
  doi={10.1080/0020717031000099029}
}
```

---

### Moreno & Osorio (2008) - *A Lyapunov approach to second-order sliding mode controllers*

- **BibTeX Key:** `moreno2008lyapunov`
- **Type:** conference
- **DOI:** 10.1109/CDC.2008.4739356
- **Conference:** 47th IEEE Conference on Decision and Control, Cancún, México, pp. 2856-2861
- **Citations:** 837+ (highly influential)
- **Used in batches:**
  - Batch 03 (Claim 1): CRITICAL - Control Theory General (Lyapunov stability with PSO gains)
  - Batch 06 (expected): CRITICAL - Super-Twisting SMC

**Key topics covered:**
- First strong Lyapunov function for super-twisting algorithm
- Finite-time convergence proofs with positive gains (k₁, k₃)
- Robustness to strong perturbations
- Performance improvement via linear correction terms

**When to use:**
- Lyapunov analysis of STA / super-twisting algorithm
- Stability proofs for second-order sliding mode control
- Gain selection guidelines for super-twisting
- Finite-time convergence claims

**BibTeX Entry:**
```bibtex
@inproceedings{moreno2008lyapunov,
  title={A Lyapunov approach to second-order sliding mode controllers and observers},
  author={Moreno, Jaime A and Osorio, Marisol},
  booktitle={2008 47th IEEE Conference on Decision and Control},
  pages={2856--2861},
  year={2008},
  organization={IEEE},
  address={Cancún, México},
  doi={10.1109/CDC.2008.4739356}
}
```

---

### Moreno & Osorio (2012) - *Strict Lyapunov Functions for the Super-Twisting Algorithm*

- **BibTeX Key:** `moreno2012strict`
- **Type:** journal
- **DOI:** 10.1109/TAC.2012.2186179
- **Journal:** IEEE Transactions on Automatic Control, Vol. 57(4), pp. 1035-1040
- **Citations:** 977+ (canonical super-twisting Lyapunov analysis)
- **Used in batches:**
  - Batch 06 (Claim 2): CRITICAL - Super-Twisting SMC (STA finite-time convergence)

**Key topics covered:**
- Family of strict Lyapunov functions for super-twisting algorithm
- Lyapunov derivative negative definiteness proof
- Finite-time convergence to second-order sliding set: $\{s=0, \dot{s}=0\}$
- Convergence time estimation
- Robustness to wider class of perturbations than classical results

**When to use:**
- THE canonical citation for super-twisting Lyapunov stability
- Finite-time convergence proofs for STA
- Second-order sliding mode Lyapunov analysis
- Strict Lyapunov function construction for higher-order SMC
- Super-twisting gain selection with Lyapunov guarantees

**BibTeX Entry:**
```bibtex
@article{moreno2012strict,
  title={Strict Lyapunov Functions for the Super-Twisting Algorithm},
  author={Moreno, Jaime A. and Osorio, Marisol},
  journal={IEEE Transactions on Automatic Control},
  volume={57},
  number={4},
  pages={1035--1040},
  year={2012},
  publisher={IEEE},
  doi={10.1109/TAC.2012.2186179}
}
```

---

## Sliding Mode Control (Advanced Texts)

### Shtessel et al. (2013) - *Sliding Mode Control and Observation*

- **BibTeX Key:** `shtessel2013sliding`
- **Type:** book
- **DOI:** 10.1007/978-0-8176-4893-0
- **Publisher:** Birkh\"{a}user (Springer)
- **Used in batches:**
  - Batch 01 (Claims 1, 3): Sliding Mode Classical
  - Batch 06 (expected): Super-Twisting

**Key topics covered:**
- Chapter 1: Introduction to sliding mode control
  - Exponential dynamics on sliding surface
  - Gain selection for finite-time convergence
  - Disturbance compensation
- Chapter 4: Super-Twisting Algorithm
  - 2nd order sliding modes
  - Continuous control design

**When to use:**
- Modern comprehensive SMC reference
- Gain design methodology
- Super-twisting implementations

**BibTeX Entry:**
```bibtex
@book{shtessel2013sliding,
  title={Sliding Mode Control and Observation},
  author={Shtessel, Yuri and Edwards, Christopher and Fridman, Leonid and Levant, Arie},
  year={2013},
  publisher={Birkh\"{a}user},
  address={New York, NY},
  doi={10.1007/978-0-8176-4893-0},
  isbn={978-0-8176-4892-3}
}
```

---

## PSO Optimization

### Kennedy & Eberhart (1995) - *Particle swarm optimization*

- **BibTeX Key:** `kennedy1995particle`
- **Type:** conference
- **DOI:** 10.1109/ICNN.1995.488968
- **Conference:** IEEE International Conference on Neural Networks
- **Used in batches:**
  - Batch 02 (expected): CRITICAL - PSO Optimization
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Original PSO algorithm formulation
- Swarm intelligence principles
- Velocity and position update rules

**When to use:**
- PSO algorithm foundations
- Original formulation citations
- Swarm intelligence theory

**BibTeX Entry:**
```bibtex
@inproceedings{kennedy1995particle,
  title={Particle swarm optimization},
  author={Kennedy, James and Eberhart, Russell},
  booktitle={Proceedings of IEEE International Conference on Neural Networks},
  volume={4},
  pages={1942--1948},
  year={1995},
  organization={IEEE},
  doi={10.1109/ICNN.1995.488968}
}
```

---

### Shi & Eberhart (1998) - *A modified particle swarm optimizer*

- **BibTeX Key:** `shi1998modified`
- **Type:** conference
- **DOI:** 10.1109/ICEC.1998.699146
- **Conference:** IEEE International Conference on Evolutionary Computation, pp. 69-73
- **Used in batches:**
  - Batch 02 (Claim 3): CRITICAL - PSO Optimization (inertia weight convergence)
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Introduction of inertia weight parameter
- Balancing exploration vs. exploitation
- Linearly decreasing inertia weight strategy
- Improved convergence properties

**When to use:**
- Inertia weight introduction/foundation
- PSO convergence improvements
- Modified PSO algorithms with adaptive parameters

**BibTeX Entry:**
```bibtex
@inproceedings{shi1998modified,
  title={A modified particle swarm optimizer},
  author={Shi, Yuhui and Eberhart, Russell},
  booktitle={Proceedings of IEEE International Conference on Evolutionary Computation},
  pages={69--73},
  year={1998},
  organization={IEEE},
  address={Alaska, USA},
  doi={10.1109/ICEC.1998.699146}
}
```

---

### Clerc & Kennedy (2002) - *The particle swarm - explosion, stability, and convergence*

- **BibTeX Key:** `clerc2002particle`
- **Type:** journal
- **DOI:** 10.1109/4235.985692
- **Journal:** IEEE Transactions on Evolutionary Computation, 6(1), 58-73
- **Used in batches:**
  - Batch 02 (Claim 1): CRITICAL - PSO Optimization (global asymptotic stability)
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Constriction factor method (χ parameter)
- PSO stability analysis in multidimensional space
- Convergence proofs and stability regions
- Velocity explosion prevention

**When to use:**
- PSO stability analysis and convergence proofs
- Global asymptotic stability claims
- Constriction coefficient applications
- Foundational PSO theory

**BibTeX Entry:**
```bibtex
@article{clerc2002particle,
  title={The particle swarm - explosion, stability, and convergence in a multidimensional complex space},
  author={Clerc, Maurice and Kennedy, James},
  journal={IEEE Transactions on Evolutionary Computation},
  volume={6},
  number={1},
  pages={58--73},
  year={2002},
  publisher={IEEE},
  doi={10.1109/4235.985692}
}
```

---

### van den Bergh & Engelbrecht (2006) - *A study of particle swarm optimization particle trajectories*

- **BibTeX Key:** `vandenbergh2006study`
- **Type:** journal
- **DOI:** 10.1016/j.ins.2005.02.003
- **Journal:** Information Sciences, 176(8), 937-971
- **Used in batches:**
  - Batch 02 (Claim 2): CRITICAL - PSO Optimization (Lyapunov stability)
  - Batch 04 (Claim 1): CRITICAL - Lyapunov Stability (PSO global asymptotic stability)
  - Batch 05 (Claim 1): CRITICAL - Inverted Pendulum (PSO ensures DIP stability)
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Lyapunov stability analysis of PSO particles
- Particle trajectory convergence proofs
- Eigenvalue analysis of PSO system matrix
- Stability with inertia weight

**When to use:**
- Lyapunov stability of PSO
- Particle convergence analysis
- Theoretical foundations of PSO stability
- Control parameter selection based on stability

**BibTeX Entry:**
```bibtex
@article{vandenbergh2006study,
  title={A study of particle swarm optimization particle trajectories},
  author={van den Bergh, Frans and Engelbrecht, Andries P.},
  journal={Information Sciences},
  volume={176},
  number={8},
  pages={937--971},
  year={2006},
  publisher={Elsevier},
  doi={10.1016/j.ins.2005.02.003}
}
```

---

### Liu et al. (2007) - *Stability Analysis of Particle Swarm Optimization*

- **BibTeX Key:** `liu2007stability`
- **Type:** conference
- **DOI:** 10.1007/978-3-540-74205-0_82
- **Conference:** ICIC 2007 - International Conference on Intelligent Computing
- **Publication:** Lecture Notes in Computer Science, vol 4682, Springer
- **Used in batches:**
  - Batch 03 (Claim 2): CRITICAL - Control Theory General (PSO convergence stability)
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Lyapunov stability analysis of PSO dynamics
- Beta parameter (β) stability conditions:
  - β < 4: PSO algorithm is stable
  - β > 4: PSO algorithm is unstable
  - β = 4: Chaotic behavior (marginal case)
- Particle trajectory convergence analysis
- Parameter selection for stable PSO operation

**When to use:**
- PSO stability conditions and parameter bounds
- Lyapunov-based PSO convergence analysis
- Beta parameter stability analysis
- Chaotic behavior in PSO systems

**BibTeX Entry:**
```bibtex
@inproceedings{liu2007stability,
  title={Stability Analysis of Particle Swarm Optimization},
  author={Liu, J. and Liu, H. and Shen, W.},
  booktitle={International Conference on Intelligent Computing (ICIC 2007)},
  series={Lecture Notes in Computer Science},
  volume={4682},
  pages={781--790},
  year={2007},
  publisher={Springer},
  address={Berlin, Heidelberg},
  doi={10.1007/978-3-540-74205-0_82}
}
```

---

### Erskine et al. (2017) - *Stochastic stability of particle swarm optimisation*

- **BibTeX Key:** `erskine2017stochastic`
- **Type:** journal
- **DOI:** 10.1007/s11721-017-0144-7
- **Journal:** Swarm Intelligence (Springer), 2017
- **Used in batches:**
  - Batch 02 (Claim 3): CRITICAL - PSO Optimization (convergence to global optimum)
  - Batch 13 (expected): HIGH - PSO Optimization

**Key topics covered:**
- Stochastic stability analysis using random dynamical systems
- Lyapunov exponent λ(α,ω) for PSO stability
- Convergence to global optimum with probability 1
- Stability region analysis for unimodal functions

**When to use:**
- Probabilistic convergence guarantees
- Global optimum convergence claims
- Stochastic PSO analysis
- Inertia weight stability conditions

**BibTeX Entry:**
```bibtex
@article{erskine2017stochastic,
  title={Stochastic stability of particle swarm optimisation},
  author={Erskine, Adam and Joyce, Thomas and Herrmann, J. Michael},
  journal={Swarm Intelligence},
  volume={11},
  number={3-4},
  pages={295--315},
  year={2017},
  publisher={Springer},
  doi={10.1007/s11721-017-0144-7}
}
```

---

## Adaptive Control

### Utkin & Poznyak (2013) - *Adaptive sliding mode control with application to super-twist algorithm*

- **BibTeX Key:** `utkin2013adaptive`
- **Type:** journal
- **DOI:** 10.1016/j.automatica.2012.09.008
- **Journal:** Automatica, vol. 49, no. 1, pp. 39-47, 2013
- **Used in batches:**
  - Batch 03 (Claim 3): CRITICAL - Control Theory General (adaptive SMC Lyapunov stability)
  - Batch 05 (expected): CRITICAL - Adaptive SMC
  - Batch 06 (expected): CRITICAL - Super-Twisting SMC

**Key topics covered:**
- Adaptive sliding mode control with equivalent control methodology
- Finite-time convergence preservation under adaptive gain adjustment
- Lyapunov stability proofs for adaptive SMC
- Super-twisting algorithm with adaptive gains
- Minimal control magnitude while maintaining sliding mode existence

**When to use:**
- Adaptive SMC Lyapunov stability claims
- Finite-time convergence with adaptive control
- Super-twisting algorithm with adaptive gains
- Equivalent control method in adaptive SMC
- Control magnitude minimization in SMC

**BibTeX Entry:**
```bibtex
@article{utkin2013adaptive,
  title={Adaptive sliding mode control with application to super-twist algorithm: Equivalent control method},
  author={Utkin, Vadim I. and Poznyak, Alexander S.},
  journal={Automatica},
  volume={49},
  number={1},
  pages={39--47},
  year={2013},
  publisher={Elsevier},
  doi={10.1016/j.automatica.2012.09.008}
}
```

---

### Ioannou & Sun (1996) - *Robust Adaptive Control*

- **BibTeX Key:** `ioannou1996robust`
- **Type:** book
- **DOI:** 10.1007/978-1-4419-8062-6
- **Publisher:** Prentice Hall

**When to use:**
- Adaptive control theory
- Parameter adaptation laws
- Robust adaptation

---

### Åström & Wittenmark (2013) - *Adaptive Control* (2nd ed.)

- **BibTeX Key:** `astrom2013adaptive`
- **Type:** book
- **Publisher:** Dover Publications
- **ISBN:** 978-0486462783

**When to use:**
- Classical adaptive control
- Self-tuning regulators
- Model reference adaptive control (MRAC)

---

## Lyapunov Stability

### Khalil (2002) - *Nonlinear Systems* (3rd ed.)

- **BibTeX Key:** `khalil2002nonlinear`
- **Type:** book
- **Publisher:** Prentice Hall
- **ISBN:** 0-13-067389-7
- **Used in batches:**
  - Batch 04 (Claim 2): CRITICAL - Lyapunov Stability (PSO maintains Lyapunov stability)

**Key topics covered:**
- Chapter 4: Lyapunov Stability Theory
- Lyapunov function construction
- LaSalle's Invariance Principle
- Stability of perturbed systems

**When to use:**
- Lyapunov stability proofs
- Stability theorems and definitions
- Nonlinear system analysis

**BibTeX Entry:**
```bibtex
@book{khalil2002nonlinear,
  title={Nonlinear Systems},
  author={Khalil, Hassan K},
  edition={3rd},
  year={2002},
  publisher={Prentice Hall},
  address={Upper Saddle River, NJ},
  isbn={0-13-067389-7}
}
```

---

### Slotine & Li (1991) - Chapter 3: Lyapunov Stability

- **BibTeX Key:** `slotine1991applied` (same book as SMC chapters)
- **Type:** book
- **Chapter:** Chapter 3

**When to use:**
- Practical Lyapunov function design
- Energy-based stability analysis
- Lyapunov equation solutions

---

## Inverted Pendulum

### Åström & Furuta (2000) - *Swinging up a pendulum by energy control*

- **BibTeX Key:** `astrom2000swinging`
- **Type:** journal
- **DOI:** 10.1016/S0005-1098(99)00140-5
- **Journal:** Automatica, 36(2), 287-295

**When to use:**
- Energy-based swing-up control
- Rotary inverted pendulum
- Nonlinear control for underactuated systems

---

### Fantoni & Lozano (2001) - *Non-linear Control for Underactuated Mechanical Systems*

- **BibTeX Key:** `fantoni2001nonlinear`
- **Type:** book
- **DOI:** 10.1007/978-1-4471-0177-2
- **Publisher:** Springer

**When to use:**
- Underactuated system theory
- Pendulum stabilization
- Swing-up plus stabilization

---

## Numerical Methods

### Press et al. (2007) - *Numerical Recipes* (3rd ed.)

- **BibTeX Key:** `press2007numerical`
- **Type:** book
- **Publisher:** Cambridge University Press

**When to use:**
- Numerical integration methods
- RK4, RK45 implementations
- General numerical algorithms

---

### Dormand & Prince (1980) - *A family of embedded Runge-Kutta formulae*

- **BibTeX Key:** `dormand1980family`
- **Type:** journal
- **DOI:** 10.1016/0771-050X(80)90013-3
- **Journal:** Journal of Computational and Applied Mathematics, 6(1), 19-26

**When to use:**
- RK45 (Dormand-Prince) method
- Adaptive step-size integration
- Embedded Runge-Kutta formulas

---

## Usage Statistics

| Citation | Total Uses | Batches | Efficiency Gain |
|----------|-----------|---------|-----------------|
| slotine1991applied | 2 | Batch 01 | 50% (2 claims, 1 source) |
| shtessel2013sliding | 2 | Batch 01 | 50% (2 claims, 1 source) |

**Overall Citation Reuse Rate:** 50% (4 claims → 2 unique sources)

---

## How to Add New Citations

When you find a citation used multiple times:

1. **Add entry to appropriate section** (SMC, PSO, Adaptive, etc.)
2. **Include complete bibliographic info** (BibTeX key, DOI, type, publisher)
3. **List batches where used** (update as you research more batches)
4. **Add "When to use" guidance** (help future researchers know when this applies)
5. **Include BibTeX entry** (for easy reference management)
6. **Update usage statistics** (track reuse efficiency)

---

**Last Updated:** 2025-10-02
**Total Citations:** 20 (added Utkin 1977, Moreno & Osorio 2012)
**Batches Completed:** 6/17 (Batches 01-06)
**Next Update:** After completing Batch 07