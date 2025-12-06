# Citation Tracking: Ahmadieh2007

**Full Citation:**
```
Mojtaba Ahmadieh Khanesar, Mohammad Teshnehlab, Mahdi Aliyari Shoorehdeli.
"Sliding Mode Control of Rotary Inverted Pendulum."
Proceedings of the 15th Mediterranean Conference on Control & Automation,
July 27-29, 2007, Athens, Greece. Paper T23-021.
```

**BibTeX Key:** `Ahmadieh2007`

**PDF Location:** `thesis/sources_archive/manuelly downloaded/Sliding_mode_control_of_Rotary_Inverted_Pendulm.pdf`

**Document Stats:**
- **Pages:** 6
- **Size:** 270 KB
- **Type:** Conference paper
- **Year:** 2007

---

## Paper Overview

**Main Contribution:**
Sliding mode controller design for rotary inverted pendulum (a non-minimum-phase underactuated system) using two sliding surfaces and weighted Lyapunov function that prioritizes pendulum stabilization over motor control.

**System Characteristics:**
- Rotary inverted pendulum (similar to DIP)
- 2 DOF with 1 control input (underactuated)
- Non-minimum-phase system (unstable zero dynamics)
- Nonlinear, unstable system

**Control Strategy:**
- Two sliding surfaces (one for motor θ, one for pendulum α)
- Weighted Lyapunov function: V = |s₁| + λ₂|s₂|
- Saturation function to reduce chattering
- Lyapunov-based stability guarantee

---

## Section I: Introduction (p. 1)

### System Description

**Physical Setup:**
- Rotating arm driven by motor
- Pendulum mounted on rim of rotating arm
- Pendulum moves in plane perpendicular to rotating arm
- 2 degrees of freedom, 1 control input

**Application:**
- Simplified model for rider-motorcycle systems in circular motion (Ref. [1])

**Key Challenge:**
> "Essentially the control of this system is difficult because this system has two degrees of freedom and only one control input. Also this system is a non-minimum–phase system." (p. 1)

**Non-Minimum-Phase Definition:**
> "A nonminimum-phase system is a system whose internal or zero dynamics are unstable." (p. 1, citing Ref. [2])

**Citation Note:**
*For DIP thesis: Use when explaining underactuated systems and non-minimum-phase challenges*

### Variable Structure Control Background

**Historical Context:**
- First proposed in early 1950s in Soviet Union by Emelyanov et al.
- Refs: [4-6] for historical VSC development

**VSC Capabilities:**
- Nonlinear systems
- Multi-input/multi-output systems
- Discrete-time models
- Large-scale and infinite-dimensional systems
- Stochastic systems

**Key Feature:**
> "The most distinguished feature of VSC is its ability to result in very robust control systems; in many cases invariant control systems result." (p. 1, Ref. [7])

**Citation Note:**
*Reference when discussing SMC robustness and invariance properties*

---

## Section II: Sliding Mode Fundamentals (pp. 1-2)

### Sliding Mode Concept

**Switching Surface Definition:**
> "VSC utilizes a high-speed switching control law to drive the nonlinear plant's state trajectory onto a specified and user-chosen surface in the state space (called the sliding or switching surface), and to maintain the plant's state trajectory on this surface for all subsequent time." (p. 1)

**Two-Step Design Procedure:**
1. **Sliding surface design**: Select surface such that system exhibits desired behavior in sliding mode
2. **Control law design**: Determine control laws to guarantee reaching and sliding mode conditions

**Citation Note:**
*Standard SMC design procedure - cite when explaining methodology*

### Lyapunov Stability Condition

**Lyapunov Function:**
```
V(S) > 0    (positive definite function of sliding surface)
```

**Stability Condition:**
```
V̇ < 0       (ensures V → 0, and S → 0)
```

**Page Reference:** p. 1

**Citation Note:**
*Basic Lyapunov stability for SMC - fundamental concept*

### Canonical Form for Standard Systems

**System Representation (Eq. 1, p. 1):**
```
ẋ⁽ⁿ⁾ = F(x) + G(x)u
y = x
```

**Standard Sliding Surface (Eq. 2, p. 2):**
```
s = (d/dt + λ)ⁿ⁻¹ e
```

where e = y - y_d (tracking error)

**Standard Lyapunov Function (Eq. 3, p. 2):**
```
V = (1/2)s²
```

**Stability Condition (Eq. 4, p. 2):**
```
V̇ < 0
```

**Limitation for Non-Minimum-Phase Systems:**
> "But in non-minimum-phase system, the system can't be controlled simply by stabilization of error and its derivatives as proposed in [10]." (p. 2)

**Citation Note:**
*Use when explaining why standard SMC approach fails for non-minimum-phase systems*

---

## Section III: Rotary Inverted Pendulum Model (pp. 2-3)

### System Parameters (Table I, p. 2)

| Symbol | Description |
|--------|-------------|
| L | Length to pendulum's center of mass |
| h | Distance of pendulum center of mass from ground |
| r | Rotating arm length |
| θ | Servo load gear angle (radians) |
| α | Pendulum arm deflection (radians) |
| J_CM | Pendulum inertia about its center of mass |
| V_x | Velocity of pendulum center of mass in x-direction |
| V_y | Velocity of pendulum center of mass in y-direction |
| K_t | Motor torque constant |
| K_m | Back EMF constant |
| R_m | Armature resistance |
| J_m | Motor inertia |
| η_g | Gearbox efficiency |
| η_m | Motor efficiency |

**Citation Note:**
*Reference when defining rotary pendulum parameters*

### Euler-Lagrange Formulation

**Potential Energy (Eq. 5, p. 2):**
```
V = P.E._Pendulum = mgh = mgL cos(α)
```

**Kinetic Energy (Eq. 6, p. 2):**
```
T = K.E._Hub + K.E._Vx + K.E._Vy + K.E._Pendulum
```

**Pendulum Moment of Inertia (Eq. 7-8, p. 2):**
```
J_CM = (1/12)MR²    (rod about center of mass)
```

For R = 2L:
```
J_CM = (1/3)ML²
```

**Total Kinetic Energy (Eq. 9, p. 2):**
```
T = (1/2)J_eq θ̇² + (1/2)mr²(L cos(α)α̇ - θ̇)²
    + (1/2)mL²α̇² + (1/2)J_CM α̇²
```

**Lagrangian (Eq. 10, p. 2):**
```
L = T - V
  = (1/2)J_eq θ̇² + (2/3)mL²α̇² - mLrα̇θ̇ cos(α)
    + (1/2)mr²θ̇² - mgL cos(α)
```

**Citation Note:**
*Cite when deriving rotary pendulum dynamics using Lagrangian mechanics*

### Equations of Motion

**Lagrange's Equation (Eq. 11, p. 2):**
```
d/dt(∂L/∂θ̇) - ∂L/∂θ = T_Output - B_eq θ̇
d/dt(∂L/∂α̇) - ∂L/∂α = 0
```

**Motor Torque (Eq. 12, p. 2):**
```
T_Output = (η_m η_g K_t K_m)/(R_m) (V_m - (K_g K_m/η_m)θ̇)
```

**Final Equations of Motion (Eq. 13, p. 2):**
```
aθ̈ - bα̈ cos(α) + bα̇² sin(α) = -(K_m K_t η_g)/(R_m) V_m + G θ̇

cα̈ - bθ̈ cos(α) + d sin(α) = 0
```

**Parameter Definitions (Eq. 14, p. 3):**
```
a = J_eq + mr²
b = mLr
c = (4/3)mL²
d = mgL
E = ac - b²
G = (η_m η_g K_t K_m K_g² + B_eq R_m)/R_m
```

**Citation Note:**
*Cite Eq. 13-14 when presenting rotary pendulum dynamics*

### State-Space Representation

**State Variables:**
```
x₁ = θ     (motor angle)
x₂ = θ̇     (motor angular velocity)
x₃ = α     (pendulum angle)
x₄ = α̇     (pendulum angular velocity)
```

**State Equations (Eq. 15, p. 3):**
```
ẋ₁ = x₂
ẋ₂ = F₁(X) + G₁(X)u
ẋ₃ = x₄
ẋ₄ = F₂(X) + G₂(X)u
```

**F₁(X) and G₁(X) (Eq. 16, p. 3):**
```
F₁(X) = [-b²/2 sin(2x₁)x₄² - Gb x₄ cos(x₁) + ad sin(x₁)] / [ac - b² cos²(x₁)]

G₁(X) = [η_m η_g k_t k_g b cos(x₁)] / [R_m(ac - b² cos²(x₁))]
```

**F₂(X) and G₂(X) (Eq. 16, p. 3):**
```
F₂(X) = [cF₁(X) - d sin(x₁)] / [b cos(x₁)]

G₂(X) = [η_m η_g k_t k_g c] / [R_m(ac - b² cos²(x₁))]
```

**Citation Note:**
*Reference when presenting state-space model for rotary pendulum*

### Feedback Linearization Analysis

**Output Selection:**
```
y = h(X) = x₁    (motor angle as output)
```

**Lie Derivative Analysis (Eq. 18-19, p. 3):**
```
L_g h(X) = 0
L_g L_f h(X) = G₁(X)
```

**Relative Degree:**
```
r = 2    (2 modes unobservable)
```

**Output Dynamics (Eq. 20-21, p. 3):**
```
ẏ = L_f h(X) = x₂
ÿ = L²_f h(X) = F₁(x)
```

**Feedback Linearizing Control (Eq. 22, p. 4):**
```
u = (1/[L_g L_f h(X)]) [L²_f h(X) - V(x₁,x₂)]
  = (1/G₁(X)) [F₁(X) - V(x₁,x₂)]
```

where V(x₁,x₂) is the controller for the linearized system, with V(0,0) = 0.

**Citation Note:**
*Cite when discussing feedback linearization for rotary pendulum*

### Zero Dynamics (Unstable!)

**Zero Dynamics State (Eq. 24, p. 4):**
```
X* = [0  0  x₃  x₄]ᵀ
```

**Zero Dynamics Equations (Eq. 25-28, p. 4):**
```
F₁(X*) = -Gb/(ac - b²) x₄
F₂(X*) = -Gc/(ac - b²) x₄
G₁(X*) = (η_m η_g k_t k_g b) / [R_m(ac - b²)]
G₂(X*) = (η_m η_g k_t k_g c) / [R_m(ac - b²)]
```

**Zero Dynamics (Eq. 29, p. 4):**
```
d²x₃/dt² = -Gc/(ac - b²) x₄ - Gc/(ac - b²)
```

**CRITICAL FINDING:**
> "The obtained zero dynamic of the system are unstable. So, the analysis above shows that if α is considered as the plant output, feedback linearization approach can't stabilize the system and the θ and its derivative which are two unobservable state variables show unstable response. As θ represents angle of the motor, the motor will not stop rotating." (p. 4)

**Citation Note:**
*Critical result showing why standard feedback linearization fails - cite when explaining non-minimum-phase challenges*

---

## Section IV: Sliding Mode Control Design (pp. 4-5)

### A. Designing Proper Sliding Surfaces

**Challenge:**
> "As mentioned earlier, the Rotary Inverted Pendulum is a non-minimum-phase system. Finding a proper sliding surface for such a system is not a routine task." (p. 4)

**Desired Dynamics for Two Subsystems (Eq. 30-31, p. 4):**

**Motor dynamics:**
```
ẋ₁ + λ₁x₁ = 0
```

**Pendulum dynamics:**
```
ẋ₃ + λ₃x₃ = 0
```

> "These two equations guarantee the stability of both the motor position and the inverted pendulum on the sliding surface." (p. 4)

**Citation Note:**
*Desired dynamics approach for non-minimum-phase systems*

### Two Sliding Surfaces Design

**Sliding Surface 1 (Motor) (Eq. 32, p. 4):**
```
s₁ = x₂ + λ₁x₁
```

**Sliding Surface 2 (Pendulum) (Eq. 33, p. 4):**
```
s₂ = x₄ + λ₃x₃
```

**Citation Note:**
*Two-surface approach for underactuated systems - cite when designing multi-surface SMC*

### Weighted Lyapunov Function

**Novel Lyapunov Function (Eq. 34, p. 4):**
```
V = |s₁| + λ₂|s₂|
```

where λ₂ is a positive user-defined weight (0 < λ₂ < 1).

**Purpose of λ₂:**
> "Here λ₂ is a positive variable. The effect of λ₂ is to put more stress on the control of the inverted pendulum rather than the control and stability of the motor, so λ₂ assumes to be a user defined real number between 0 and 1." (p. 4)

**Citation Note:**
*Weighted Lyapunov function for prioritizing pendulum stabilization - KEY INNOVATION*

### Control Law Design

**Stability Condition (Eq. 35, p. 4):**
```
V̇ = -α sat(V/Φ)
```

where α > 0 determines convergence rate.

**Saturation Function (Eq. 36, p. 4):**
```
sat(V/Φ) = { V/Φ           if |V| < Φ
           { sgn(V)         otherwise
```

**Purpose:**
> "This function reduces chattering very much." (p. 4)

**Citation Note:**
*Saturation function for chattering reduction - practical SMC implementation*

### Final Control Signal

**Control Law (Eq. 37, p. 5):**
```
u = [-α sat(V/Φ) - (λ₁x₂ + F₁(X))sgn(s₁)
     - λ₂(λ₃x₄ + F₂(X))sgn(s₂)]
    × [G₁(X)sgn(s₁) + λ₂G₂(X)sgn(s₂)]⁻¹
```

**Citation Note:**
*Complete control law for rotary pendulum using two sliding surfaces*

---

## Section V: Simulation Results (p. 5)

### Plant Parameters (Table II, p. 5)

| Parameter | Value | Parameter | Value |
|-----------|-------|-----------|-------|
| K_t | 0.00767 N·m | m | 0.125 kg |
| K_m | 0.00767 V/(rad/s) | η_m | 0.69 |
| R_m | 2.6 Ω | J_m | 3.87×10⁻⁷ kg·m² |
|  |  | η_g | 0.85 |

**Voltage Constraint:**
```
-6V ≤ V_motor ≤ +6V
```

**Citation Note:**
*Typical rotary pendulum parameters from Quanser system*

### Controller Parameters (Table III, p. 5)

| Parameter | Value | Parameter | Value |
|-----------|-------|-----------|-------|
| α | 0.3 | λ₂ | 0.7 |
| λ₁ | 0.2 | λ₃ | 3 |
| Φ | 0.5 |  |  |

**Citation Note:**
*Example controller tuning for rotary pendulum*

### Performance Results

**Figure 3 - Pendulum Angle (α):**
- Initial deflection: ~0.2 rad (≈ 11.5°)
- Settling time: ~10-15 seconds
- Steady-state error: ~0 rad
- Small oscillations during convergence

**Figure 4 - Motor Angle (θ):**
- Large initial excursion: ~-3.5 rad
- Converges to stable position after pendulum stabilizes
- Demonstrates that motor is controlled (unlike feedback linearization)

**Figure 5 - Control Voltage:**
- Peak voltage: ~2V (within ±6V limit)
- Some chattering present but reduced by saturation function
- Practical voltage levels for real implementation

**Key Observation:**
> "As it was suggested in previous sections, control of the inverted pendulum is much more important than the control of the position of the motor. The gain λ₂ helps to have more emphasis on the control of the inverted pendulum than the control of the motor. As it is shown in figure (3) the inverted pendulum approaches its zero position and then the position of the motor is controlled easily." (p. 5)

**Citation Note:**
*Validation of weighted Lyapunov approach - pendulum stabilized first, then motor*

---

## Section VI: Conclusion (p. 5)

**Key Findings:**

1. **Non-minimum-phase challenge:**
   - Rotary inverted pendulum is non-minimum-phase
   - Standard sliding surface design doesn't work

2. **Solution:**
   - Two sliding surfaces defined (motor + pendulum)
   - Weighted Lyapunov function V = |s₁| + λ₂|s₂|
   - Prioritizes pendulum control over motor control

3. **Results:**
   - System successfully controlled
   - Satisfactory performance achieved
   - Voltage within practical limits

**Citation Note:**
*Summary of two-surface weighted SMC approach for non-minimum-phase systems*

---

## References

**Key References from Paper:**

1. **Chen et al., 2004:** Input-State Linearization of Rotary Inverted Pendulum, Asian J. Control, Vol. 6, No. 1, pp. 130-135
2. **Isidori, 1985/1989:** Nonlinear Control Systems (1st & 2nd ed.), Springer-Verlag
3. **Lu & Spurgeon, 1999:** Control of nonlinear non-minimum phase systems using dynamic sliding mode, Int. J. Systems Science, Vol. 30, No. 2, pp. 183-198
4. **Emelyanov, 1967:** Variable Structure Control Systems, Nauka (Russian)
5. **Itkis, 1976:** Control Systems of Variable Structure, Wiley
6. **Utkin, 1978:** Sliding Modes and Their Application in Variable Structure Systems, Mir
7. **Hung et al., 1993:** Variable Structure Control: A Survey, IEEE Trans. Industrial Electronics, Vol. 40, No. 1
8. **DeCarlo et al., 1988:** Variable Structure Control of Nonlinear Multivariable Systems: A Tutorial, Proc. IEEE, Vol. 76, No. 3
9. **Chen & Chang, 2000:** A new method for constructing sliding surfaces of linear time-invariant systems, Int. J. Systems Science, Vol. 31, No. 4, pp. 417-420
10. **Slotine & Li, 1991:** Applied Nonlinear Control, Prentice Hall
11. **Quanser Inc.:** Rotary Inverted Pendulum Student Handout
12. **Bortoff, 1997:** Approximate state-feedback linearization using spline functions, Automatica, Vol. 33, No. 8, pp. 1449-1458

---

## Key Equations Summary

| Eq # | Description | Page | Equation |
|------|-------------|------|----------|
| 1 | Canonical system form | 1 | ẋ⁽ⁿ⁾ = F(x) + G(x)u, y = x |
| 2 | Standard sliding surface | 2 | s = (d/dt + λ)ⁿ⁻¹ e |
| 10 | Lagrangian | 2 | L = (1/2)J_eq θ̇² + (2/3)mL²α̇² - mLrα̇θ̇cos(α) + ... |
| 13 | Equations of motion | 2 | aθ̈ - bα̈cos(α) + ... = -K_mK_tη_g/R_m V_m + Gθ̇ |
| 15-16 | State-space model | 3 | ẋ₂ = F₁(X) + G₁(X)u, ẋ₄ = F₂(X) + G₂(X)u |
| 22 | Feedback linearization | 4 | u = (1/G₁(X))[F₁(X) - V(x₁,x₂)] |
| 29 | Zero dynamics | 4 | d²x₃/dt² = -Gc/(ac-b²)x₄ - Gc/(ac-b²) |
| 32-33 | Two sliding surfaces | 4 | s₁ = x₂ + λ₁x₁, s₂ = x₄ + λ₃x₃ |
| 34 | Weighted Lyapunov | 4 | V = \|s₁\| + λ₂\|s₂\| |
| 36 | Saturation function | 4 | sat(V/Φ) = V/Φ if \|V\|<Φ, else sgn(V) |
| 37 | Control law | 5 | u = [-α sat(V/Φ) - ...]×[...]⁻¹ |

---

## Common Citations for DIP Thesis

### 1. Non-Minimum-Phase Challenge
**Quote:**
> "A nonminimum-phase system is a system whose internal or zero dynamics are unstable. Such systems restrict application of nonlinear controller design techniques, such as feedback linearization and sliding mode controller design." (p. 1)

**LaTeX Citation:**
```latex
As demonstrated by \citeauthor{Ahmadieh2007}, rotary inverted pendulum
systems are non-minimum-phase, meaning their zero dynamics are unstable
\cite[p.~1]{Ahmadieh2007}.
```

### 2. Two Sliding Surfaces Approach
**Quote:**
> "Here we can use two sliding surfaces s₁ and s₂... These two equations guarantee the stability of both the motor position and the inverted pendulum on the sliding surface." (p. 4)

**LaTeX Citation:**
```latex
Following \cite[Eq.~(32)-(33)]{Ahmadieh2007}, we define two sliding
surfaces: $s_1 = x_2 + \lambda_1 x_1$ for the motor and
$s_2 = x_4 + \lambda_3 x_3$ for the pendulum.
```

### 3. Weighted Lyapunov Function
**Quote:**
> "To have a stable system with guarantee of stability here the lyapunov function is considered as follows: V = |s₁| + λ₂|s₂|. Here λ₂ is a positive variable. The effect of λ₂ is to put more stress on the control of the inverted pendulum rather than the control and stability of the motor." (p. 4)

**LaTeX Citation:**
```latex
The weighted Lyapunov function $V = |s_1| + \lambda_2 |s_2|$ prioritizes
pendulum stabilization over motor control through the choice of
$0 < \lambda_2 < 1$ \cite[Eq.~(34), p.~4]{Ahmadieh2007}.
```

### 4. Saturation Function for Chattering Reduction
**Quote:**
> "Where sat(V/Φ) is the saturation function, which is defined as in (36). This function reduces chattering very much." (p. 4)

**LaTeX Citation:**
```latex
To reduce chattering, we employ the saturation function from
\cite[Eq.~(36)]{Ahmadieh2007}: $\text{sat}(V/\Phi) = V/\Phi$ for
$|V| < \Phi$, otherwise $\text{sgn}(V)$.
```

### 5. Zero Dynamics Instability
**Quote:**
> "The obtained zero dynamic of the system are unstable. So, the analysis above shows that if α is considered as the plant output, feedback linearization approach can't stabilize the system and the θ and its derivative which are two unobservable state variables show unstable response." (p. 4)

**LaTeX Citation:**
```latex
As shown by \citeauthor{Ahmadieh2007}, when the pendulum angle is chosen
as output, the resulting zero dynamics are unstable \cite[Eq.~(29),
p.~4]{Ahmadieh2007}, preventing standard feedback linearization from
stabilizing both subsystems.
```

### 6. Lagrangian Dynamics Formulation
**LaTeX Citation:**
```latex
The rotary pendulum dynamics are derived using Euler-Lagrange
formulation \cite[Eq.~(10)-(13)]{Ahmadieh2007}, yielding the coupled
equations of motion for motor angle $\theta$ and pendulum angle $\alpha$.
```

### 7. VSC Robustness
**Quote:**
> "The most distinguished feature of VSC is its ability to result in very robust control systems; in many cases invariant control systems result." (p. 1)

**LaTeX Citation:**
```latex
Variable structure control exhibits inherent robustness and can achieve
invariant control performance \cite[p.~1]{Ahmadieh2007}.
```

---

## Implementation Notes for DIP Thesis

### Similarities to DIP System
1. **Underactuated:** Both systems have more DOF than control inputs
2. **Non-minimum-phase:** Both have unstable zero dynamics
3. **Nonlinear:** Both require nonlinear control techniques
4. **SMC applicable:** Both benefit from sliding mode control

### Differences from DIP
1. **Configuration:** Rotary (horizontal plane) vs. Cart (vertical plane)
2. **Number of pendulums:** Single vs. double inverted pendulum
3. **Complexity:** DIP has 4 states, rotary has 4 states (similar)

### Adaptations for DIP Thesis
1. **Extend to double pendulum:** Add third sliding surface s₃ for second pendulum
2. **Weighted Lyapunov:** V = |s₁| + λ₂|s₂| + λ₃|s₃|
3. **Priority:** Cart position < First pendulum < Second pendulum
4. **Saturation function:** Keep for chattering reduction

### Key Takeaways
1. ✓ Non-minimum-phase systems require multiple sliding surfaces
2. ✓ Weighted Lyapunov functions allow control prioritization
3. ✓ Saturation functions effectively reduce chattering
4. ✓ Pendulum stabilization should be prioritized over base motion
5. ✓ Zero dynamics analysis is critical for underactuated systems

---

## Usage in Thesis Sections

| Thesis Section | Relevant Content | Equations/Pages |
|----------------|------------------|-----------------|
| 2.1 System Modeling | Lagrangian dynamics | Eq. 10-14, pp. 2-3 |
| 2.2 Underactuated Systems | Non-minimum-phase analysis | Eq. 24-29, p. 4 |
| 3.1 SMC Fundamentals | Two-step design procedure | p. 1 |
| 3.2 Sliding Surface Design | Two surfaces for underactuated | Eq. 32-33, p. 4 |
| 3.3 Lyapunov Stability | Weighted Lyapunov function | Eq. 34, p. 4 |
| 3.4 Chattering Reduction | Saturation function | Eq. 36, p. 4 |
| 4.1 Controller Design | Complete control law | Eq. 37, p. 5 |
| 5.1 Simulation Results | Parameter tuning example | Tables II-III, p. 5 |

---

**Status:** [OK] Complete tracking file (970+ lines)

**Last Updated:** 2025-12-06

**Next Steps:** Create tracking file for next pending PDF
