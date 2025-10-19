# II. RELATED WORK

This section reviews the state-of-the-art in sliding mode control chattering mitigation (Section II-A), particle swarm optimization for controller tuning (Section II-B), adaptive boundary layer techniques (Section II-C), and positions our contributions within the existing literature (Section II-D).

## A. SMC Chattering Mitigation Approaches

Chattering remains the primary barrier to widespread SMC adoption in industrial mechatronic systems. Recent research has explored several mitigation strategies:

**Higher-Order Sliding Mode Control (HOSMC):** Levant's super-twisting algorithm (STA) and other higher-order methods achieve continuous control inputs by driving higher derivatives of the sliding variable to zero. Recent work by Ayinalem et al. (2025) demonstrated PSO-tuned STA-SMC for robotic trajectory tracking, showing improved chattering reduction compared to first-order SMC. However, HOSMC requires additional state measurements or observers, increasing implementation complexity and computational burden.

**Fuzzy-Adaptive Techniques:** Several 2024 studies combined fuzzy logic with SMC to adaptively adjust control parameters. A fuzzy-adaptive second-order SMC for inverted pendulum systems (Frontiers, 2024) reported significant chattering suppression and improved robustness. Similarly, a self-regulating fuzzy-adaptive SMC (SFA-SMC) for rotary pendulum systems enhanced disturbance rejection while reducing chattering content. The fuzzy rules provide smooth interpolation between control modes, but parameter tuning remains heuristic and lacks theoretical stability guarantees.

**Observer-Based Designs:** Extended state observers (ESO) and disturbance observers estimate unmatched disturbances, enabling compensation without excessive switching gain. A 2023 study on rotary inverted pendulum stabilization used observer-based SMC to achieve better performance with chattering alleviation. However, observer design introduces additional dynamics that may affect transient response.

**Hybrid Control Frameworks:** Recent work (Scientific Reports, December 2024) combined optimized fuzzy logic controllers with SMC for rotary inverted pendulums, leveraging complementary strengths. While promising for specific systems, these hybrid approaches lack generalizability and require significant domain expertise for tuning.

**Limitation:** Existing approaches either sacrifice tracking precision (fuzzy-adaptive), increase complexity (HOSMC, observers), or rely on heuristic tuning (hybrid). None provide a principled optimization framework for balancing chattering reduction against control performance.

## B. Particle Swarm Optimization for Controller Tuning

PSO has emerged as an effective metaheuristic for SMC parameter optimization due to its derivative-free nature and global search capabilities:

**Recent Applications (2023-2025):** A comprehensive review (Springer, 2024) synthesized PSO-SMC integration strategies for autonomous vehicles, highlighting super-twisting SMC optimization. PSO-tuned STSMC for articulated robots (Wiley, 2025) achieved optimal parameter values ensuring consistency, stability, and robustness. A hybrid enhanced PSO (HEPSO-SMC) for manipulators (Nature Scientific Reports, 2025) optimized parameters $c_1, c_2, \epsilon, k$, outperforming standard PSO-SMC and improved PSO variants.

**Advantages Over Manual Tuning:** PSO eliminates trial-and-error by systematically exploring high-dimensional parameter spaces. Unlike gradient-based methods, PSO handles non-convex, non-smooth fitness landscapes common in control system optimization. Recent work on third-order SMC for quadcopters (MDPI, 2025) demonstrated PSO's effectiveness for fine-tuning gain values in trajectory tracking applications.

**Existing Fitness Functions:** Most PSO-SMC studies optimize single objectives (e.g., tracking error minimization) or use ad-hoc weighted sums without justification. For example, HEPSO-SMC weighted multiple objectives but provided no rationale for weight selection. Critically, **all reviewed studies validated controllers only under training conditions**, failing to assess robustness beyond the optimization domain.

**Gap Identified:** No prior work systematically optimizes adaptive boundary layer parameters using PSO with a chattering-weighted fitness function, nor do existing studies report generalization failures when initial conditions exceed the training distribution.

## C. Adaptive Boundary Layer Techniques

The boundary layer method replaces the discontinuous signum function with a continuous saturation function within a boundary layer of thickness $\epsilon$, trading chattering for steady-state error:

**Self-Regulated Boundary Layers:** An IEEE study proposed adaptive SMC with self-regulated boundary layer considering actuator saturation and error tolerance. The boundary layer adapts based on tracking error magnitude, but parameter update laws were heuristically designed without Lyapunov stability analysis.

**Dynamic Adjustment Approaches:** Recent work (2022-2024) combined adaptive laws with SMC to adjust boundary layers dynamically. A 2024 ship course control study implemented adaptive complementary SMC with boundary layer realizing dynamic changes to ensure robustness. However, the adaptation mechanisms lack systematic optimization and rely on designer-specified gains.

**Fuzzy Boundary Layer Tuning:** Fuzzy rules optimize SMC signals and adaptively adjust boundary layers to compensate uncertainty (2023 excavator hydraulic position control). While effective for specific applications, fuzzy approaches require extensive expert knowledge for rule base design and lack generalizability.

**Theoretical Limitations Acknowledged:** The literature notes that boundary layer techniques lose finite-time convergence within the boundary layer, achieving only practical stabilization with accuracy dependent on continuous function parameters. This tradeoff between chattering reduction and tracking precision motivates our PSO-based systematic optimization.

**Gap Identified:** Existing adaptive boundary layer methods use heuristic adaptation laws without principled optimization. No prior work optimizes boundary layer parameters using metaheuristic algorithms (e.g., PSO) to minimize chattering while maintaining control performance, nor do studies provide rigorous Lyapunov stability analysis for time-varying boundary layers.

## D. Research Gap and Positioning

Table I compares our approach with representative recent work, highlighting key distinctions:

**TABLE I: COMPARISON WITH STATE-OF-THE-ART SMC APPROACHES**

| Reference | Year | System | Technique | Chattering Mitigation | Parameter Tuning | Validation Scope | Limitation Acknowledged |
|-----------|------|--------|-----------|----------------------|-----------------|------------------|------------------------|
| Ayinalem et al. [1] | 2025 | Robot manipulator | PSO-tuned STA-SMC | Higher-order SMC | PSO (tracking error) | Single scenario (nominal) | No generalization testing |
| HEPSO-SMC [2] | 2025 | Manipulator | Hybrid enhanced PSO-SMC | Gain optimization | HEPSO (c₁,c₂,ε,k) | Training distribution only | Ad-hoc weight selection |
| Frontiers 2024 [3] | 2024 | Inverted pendulum | Fuzzy adaptive 2nd-order SMC | Fuzzy + higher-order | Manual fuzzy rules | Nominal conditions | Heuristic rule design |
| SFA-SMC [4] | 2024 | Rotary pendulum | Self-regulating fuzzy-adaptive | Fuzzy interpolation | Trial-and-error | Small perturbations | No stability proof |
| Sci Reports 2024 [5] | 2024 | Rotary pendulum | Optimized FLC + SMC hybrid | Fuzzy optimization | GA (fuzzy params) | Single operating point | Lacks generalizability |
| IEEE Self-Reg [6] | 2018 | Generic nonlinear | Self-regulated boundary layer | Adaptive boundary | Heuristic adaptive law | Simulation only | No systematic optimization |
| **Our Work** | **2025** | **Double inverted pendulum** | **PSO-optimized adaptive boundary layer** | **Dynamic ε adjustment** | **PSO (chattering-weighted)** | **Multi-scenario (±0.05, ±0.3 rad)** | **Honest reporting: 50.4× generalization failure** |

**Key Distinctions:**

1. **Systematic Optimization:** We are the first to apply PSO specifically to adaptive boundary layer parameter optimization ($\epsilon_{\min}, \alpha$) with a chattering-weighted fitness function (70% chattering + 15% settling + 15% overshoot), providing principled weight selection rationale.

2. **Lyapunov Stability for Adaptive Boundary Layer:** We provide rigorous Lyapunov analysis proving finite-time convergence is preserved with time-varying $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$, addressing the theoretical gap in prior adaptive boundary layer work.

3. **Multi-Scenario Validation:** Unlike all reviewed studies that validate only on training distributions, we systematically test robustness under 6× larger initial conditions (±0.3 rad vs. ±0.05 rad training), exposing catastrophic generalization failure.

4. **Honest Negative Results:** We quantitatively report failures (50.4× chattering degradation, 90.2% failure rate, 0% disturbance rejection) rarely disclosed in prior literature, providing actionable insights for future robust optimization research.

**Research Gap Summary:**
- **Gap 1:** No prior work optimizes adaptive boundary layer parameters using PSO with chattering-prioritized fitness functions
- **Gap 2:** Existing adaptive boundary layer methods lack Lyapunov stability proofs for time-varying boundary thickness
- **Gap 3:** Single-scenario validation is ubiquitous; robustness testing beyond training distributions is absent
- **Gap 4:** Generalization failures and disturbance rejection limitations are underreported in SMC literature

**Our Contributions Address These Gaps:** By combining PSO optimization, Lyapunov-proven stability, multi-scenario validation, and honest failure reporting, this work advances the state-of-the-art in practical SMC design and establishes best practices for robust controller validation.

---

## Summary

This section reviewed recent advances in:
1. **Chattering mitigation** (Section II-A): HOSMC, fuzzy-adaptive, observers, hybrids—all with heuristic tuning
2. **PSO for SMC** (Section II-B): Effective for parameter optimization, but lacks chattering-focused fitness functions and multi-scenario validation
3. **Adaptive boundary layers** (Section II-C): Dynamic adjustment methods exist, but without systematic optimization or rigorous stability analysis
4. **Research gaps** (Section II-D): Table I comparison shows our work uniquely combines PSO-optimized adaptive boundary layers, Lyapunov stability analysis, multi-scenario validation, and honest negative result reporting

**Next:** Section III presents the double inverted pendulum system model used for controller design and validation.

---

## References (Placeholder - Full BibTeX in separate file)

[1] Ayinalem et al., "PSO Tuned Super-Twisting Sliding Mode Controller for Trajectory Tracking Control of an Articulated Robot," *Journal of Electrical and Computer Engineering*, 2025.

[2] et al., "HEPSO-SMC: A Sliding Mode Controller Optimized by Hybrid Enhanced Particle Swarm Algorithm for Manipulators," *Scientific Reports*, vol. 15, 2025.

[3] "Second-Order Sliding Mode Optimization Control of an Inverted Pendulum System Based on Fuzzy Adaptive Technology," *Frontiers in Mechanical Engineering*, 2024.

[4] "Stabilization Control of Rotary Inverted Pendulum Using a Novel EKF-Based Fuzzy Adaptive Sliding-Mode Controller," *Automatic Control and Computer Sciences*, vol. 58, 2024.

[5] "Optimized Fuzzy Logic and Sliding Mode Control for Stability and Disturbance Rejection in Rotary Inverted Pendulum," *Scientific Reports*, vol. 14, Dec. 2024.

[6] "An Adaptive Sliding Mode Control with Self-Regulated Boundary Layer," *IEEE Conference*, 2018.
