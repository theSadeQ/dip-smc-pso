# Shtessel2014 Citation Tracking

**PDF File**: `Shtessel2014_Sliding_Mode_Control_Observation.pdf`
**Extracted Text**: `extracted_text/Shtessel2014_Sliding_Mode_Control_Observation.txt`
**PDF Size**: 8.6 MB
**Text Size**: 19,064 lines, 620 KB
**PDF Status**: [EXTRACTED] High-quality text extraction
**BibTeX Key**: `Shtessel2014`
**Full Title**: Sliding Mode Control and Observation
**Authors**: Yuri Shtessel, Christopher Edwards, Leonid Fridman, Arie Levant
**Publisher**: Springer (Birkhäuser), New York
**Year**: 2014
**ISBN**: 978-0-8176-4892-3 (hardback), 978-0-8176-4893-0 (eBook)
**DOI**: 10.1007/978-0-8176-4893-0
**Series**: Control Engineering
**Pages**: Approx. 500+ pages

**Date Created**: 2025-12-07
**Last Updated**: 2025-12-07

---

## Document Overview

This comprehensive textbook covers sliding mode control (SMC) theory from first principles to state-of-the-art higher-order sliding modes (HOSM). Written by four leading SMC researchers, it provides rigorous mathematical treatment with practical examples, Matlab/Simulink implementations, and real-world case studies.

**Key Topics**:
- Conventional sliding mode control (Chapters 1-2)
- Sliding mode observers and differentiators (Chapter 3)
- Second-order sliding modes (2-SM) including super-twisting (Chapter 4)
- Robustness to parasitic dynamics (Chapter 5)
- Higher-order sliding modes (HOSM) (Chapter 6)
- HOSM observers and identification (Chapter 7)
- Applications: power converters, motors, aircraft, robotics (Chapter 8+)

**Relevance to DIP Thesis**: FOUNDATIONAL reference for all SMC variants implemented (classical, super-twisting, adaptive, hybrid adaptive STA-SMC). Chapters 1, 2, 4, and 6 are CRITICAL.

---

## Document Structure

| Chapter | Pages | Content Summary |
|---------|-------|-----------------|
| Chapter 1 | ~1-48 | Intuitive SMC introduction (tutorial level) |
| Chapter 2 | ~49-102 | Conventional SMC (rigorous, Lyapunov-based) |
| Chapter 3 | ~103-142 | Conventional sliding mode observers (CSMO) |
| Chapter 4 | ~143-184 | Second-order sliding modes (2-SM, super-twisting) |
| Chapter 5 | ~185-204 | Robustness to parasitic dynamics (frequency domain) |
| Chapter 6 | ~205-250 | Higher-order sliding modes (HOSM) |
| Chapter 7 | ~251-286 | HOSM observers and identification |
| Chapter 8 | ~287-320+ | Applications and case studies |

**Total**: Approx. 500+ pages, 8 chapters, numerous examples and exercises

---

## Tracked Content

### Chapter 1: Intuitive Introduction to SMC (Tutorial Level)

**Used in Thesis**: Section 2.3 (Literature Review - SMC), Section 4.1 (SMC Theory Introduction)

**Content Summary**:
Introduces SMC concepts using basic control theory without requiring advanced mathematics. Covers sliding variable design, reaching and sliding phases, chattering avoidance, equivalent control, matching condition, sliding mode observers, second-order sliding modes, and output tracking via relative degree approach.

**LaTeX Citations**:
```latex
% General SMC introduction
Sliding mode control provides robustness to matched disturbances \cite[Ch.~1]{Shtessel2014}.

% Chattering elimination
Quasi-sliding mode using boundary layer \cite[Sec.~1.2.1]{Shtessel2014} eliminates chattering by replacing sign() with sat().

% Equivalent control concept
The equivalent control \cite[Sec.~1.3]{Shtessel2014} represents the average value of discontinuous control.

% Matching condition
The matching condition \cite[Sec.~1.5]{Shtessel2014} determines which disturbances can be rejected by SMC.

% Second-order sliding mode (2-SM)
Second-order sliding modes \cite[Sec.~1.7]{Shtessel2014} drive both s and ds/dt to zero, reducing chattering.
```

**Key Sections**:
- **1.1 Main Concepts** (line ~279): Sliding surface, reaching phase, sliding phase
- **1.2 Chattering Avoidance** (line ~511): Boundary layer (quasi-sliding), asymptotic SMC
- **1.3 Equivalent Control** (line ~701): Average control value on sliding surface
- **1.4 Sliding Mode Equations** (line ~748): Reduced-order dynamics on manifold
- **1.5 Matching Condition** (line ~802): Insensitivity to matched disturbances
- **1.6 SMC Observer/Differentiator** (line ~828): State estimation, unknown input reconstruction
- **1.7 Second-Order Sliding Mode** (line ~923): 2-SM concept, chattering reduction
- **1.8 Output Tracking** (line ~1036): Relative degree approach for tracking control

**Important Points**:
- Tutorial-level introduction suitable for beginners
- Graphical explanations and simulation plots
- Advantages: robustness, finite-time convergence, reduced-order dynamics
- Chattering: causes, elimination (boundary layer), attenuation (asymptotic SMC)

---

### Chapter 2: Conventional Multivariable SMC (Rigorous Treatment)

**Used in Thesis**: Section 4.2 (Classical SMC Design), Section 4.3 (SMC Stability Analysis)

**Content Summary**:
Rigorous formulation of conventional SMC using linear algebra and Lyapunov techniques. Covers Filippov solutions, equivalent control, sliding surface design (eigenvalue placement, LQR), relay control, unit-vector control, output-feedback SMC, and integral sliding modes (ISM).

**LaTeX Citations**:
```latex
% Filippov solution for discontinuous systems
Filippov solution concept \cite[Sec.~2.1.1]{Shtessel2014} handles discontinuous differential equations rigorously.

% Sliding surface design via eigenvalue placement
Sliding surface design via eigenvalue placement \cite[Sec.~2.2.2]{Shtessel2014} ensures desired closed-loop dynamics.

% LQR-based sliding surface
LQR-based sliding surface design \cite[Sec.~2.2.3]{Shtessel2014} minimizes quadratic performance index.

% Unit-vector control
Unit-vector control law \cite[Sec.~2.4]{Shtessel2014} provides robustness to matched and unmatched uncertainties.

% Integral sliding mode (ISM)
Integral sliding mode \cite[Sec.~2.7]{Shtessel2014} eliminates reaching phase and maintains system order.
```

**Key Sections**:
- **2.1 Introduction** (line ~1585): Filippov solution, equivalent control revisited
- **2.2 Sliding Surface Design** (line ~2019): Regular form, eigenvalue placement, LQR
- **2.3 Relay Control Law** (line ~3029): Single-input, multi-input, perturbed systems
- **2.4 Unit-Vector Control** (line ~3430): Matched/unmatched uncertainty
- **2.5 Output Tracking with Integral Action** (line ~4126): Integral augmentation
- **2.6 Output-Based Hyperplane** (line ~4265): Static/dynamic output feedback
- **2.7 Integral Sliding Mode (ISM)** (line ~4936): No reaching phase, full-order dynamics

**Important Theorems/Lemmas**:
- Regular form transformation → Sec. 2.2.1
- Eigenvalue placement theorem → Sec. 2.2.2
- LQR sliding surface existence → Sec. 2.2.3
- Unit-vector control stability → Sec. 2.4
- ISM robustness properties → Sec. 2.7

**Relevance to Thesis**:
- Classical SMC design (eigenvalue placement) → Controller 1
- ISM for disturbance compensation → Future work consideration

---

### Chapter 3: Conventional Sliding Mode Observers (CSMO)

**Used in Thesis**: Future work (not currently implemented, but relevant for sensor fusion)

**Content Summary**:
Detailed coverage of sliding mode observers for state estimation and unknown input reconstruction. Covers simple SMO design, robustness properties, and various CSMO architectures using Lyapunov techniques.

**LaTeX Citations**:
```latex
% Simple sliding mode observer
Simple sliding mode observer \cite[Sec.~3.2]{Shtessel2014} estimates states while reconstructing disturbances.

% CSMO robustness
Robustness properties of CSMO \cite[Sec.~3.3]{Shtessel2014} enable accurate state estimation under uncertainty.
```

**Key Sections**:
- **3.1 Introduction** (line ~5631): Motivation for SMO
- **3.2 Simple SMO** (line ~5658): Basic observer design
- **3.3 Robustness Properties** (line ~5921): Uncertainty rejection

**Relevance to Thesis**:
- Future extension: CSMO for DIP state estimation with noisy sensors

---

### Chapter 4: Second-Order Sliding Modes (2-SM) - CRITICAL FOR THESIS

**Used in Thesis**: Section 4.5 (Super-Twisting Algorithm), Section 4.6 (Hybrid Adaptive STA-SMC)

**Content Summary**:
Comprehensive treatment of 2-SM control algorithms including twisting, super-twisting (STA), suboptimal, prescribed convergence law, and quasi-continuous controllers. Emphasizes finite-time convergence, chattering attenuation, and enhanced discrete-time accuracy (O(T²)).

**LaTeX Citations**:
```latex
% 2-SM finite-time convergence
Second-order sliding modes \cite[Ch.~4]{Shtessel2014} drive both s and ds/dt to zero in finite time.

% Super-twisting algorithm (STA)
The super-twisting algorithm \cite[Sec.~4.X]{Shtessel2014} requires only sliding variable measurement (not derivative).

% Variable-gain super-twisting
Variable-gain super-twisting \cite[Sec.~4.7]{Shtessel2014} adapts gains online to disturbance magnitude.

% Chattering attenuation in 2-SM
2-SM controllers \cite[Ch.~4]{Shtessel2014} significantly attenuate chattering compared to conventional SMC.

% Discrete-time accuracy
Computer-implemented 2-SM \cite[Ch.~4]{Shtessel2014} provides accuracy proportional to T², where T is sampling time.
```

**Key Sections**:
- **4.1 Introduction to 2-SM**: Motivation, definitions, properties
- **4.2 Twisting Algorithm**: Requires s and ds/dt measurement
- **4.3 Super-Twisting Algorithm (STA)**: Requires ONLY s measurement (not derivative!)
- **4.4 Suboptimal Algorithm**: Minimizes convergence time
- **4.5 Prescribed Convergence Law**: Custom convergence trajectory
- **4.6 Quasi-Continuous Algorithm**: Further chattering reduction
- **4.7 Variable-Gain Super-Twisting** (line ~170-179): Adaptive gain selection
- **4.8 Output Regulation via 2-SM**: Tracking control application
- **4.9 Notes and References** (line ~179): Historical context, further reading
- **4.10 Exercises** (line ~182): Homework problems

**Super-Twisting Algorithm (STA) - CORE THESIS CONTROLLER**:
```
Control law (typical form):
u = -λ₁ |s|^(1/2) sign(s) + u₁
u̇₁ = -λ₂ sign(s)

Where:
- s: sliding variable (measured)
- λ₁, λ₂: positive gains
- sign(s): signum function
```

**Variable-Gain STA** (Sec. 4.7, line ~170-179):
```
Gains adapt online:
λ₁ = λ₁(|s|), λ₂ = λ₂(|s|)

Advantages:
- Automatic adaptation to disturbance level
- Eliminates need for disturbance bound knowledge
- Balances performance vs. chattering
```

**Relevance to Thesis**:
- **STA-SMC controller** (thesis controller #2) → Sec. 4.3, 4.7
- **Hybrid Adaptive STA-SMC** (thesis controller #4) → Sec. 4.7 + adaptive extensions
- Chattering reduction via 2-SM → Performance comparison
- Discrete-time accuracy O(T²) → Simulation validation

---

### Chapter 5: Robustness to Parasitic Dynamics

**Used in Thesis**: Section 5.3 (Robustness Analysis - Unmodeled Dynamics)

**Content Summary**:
Analyzes conventional SMC and 2-SM robustness to parasitic (unmodeled) dynamics using frequency-domain techniques. Uses describing function method to estimate switching oscillation amplitude and frequency.

**LaTeX Citations**:
```latex
% Describing function analysis
Describing function technique \cite[Ch.~5]{Shtessel2014} estimates chattering amplitude and frequency.

% 2-SM robustness to parasitic dynamics
Super-twisting robustness to parasitic dynamics \cite[Ch.~5]{Shtessel2014} is analyzed via frequency domain.
```

**Relevance to Thesis**:
- Validates SMC robustness to neglected dynamics (e.g., actuator dynamics, friction)
- Explains chattering behavior in presence of parasitic dynamics

---

### Chapter 6: Higher-Order Sliding Modes (HOSM)

**Used in Thesis**: Section 2.3 (Literature Review - HOSM), Future work reference

**Content Summary**:
Generalizes 2-SM to arbitrary order k. Covers nested SMC, quasi-continuous HOSM, homogeneity and contractivity-based design, arbitrary-order robust differentiators. Applications to systems with arbitrary relative degree.

**LaTeX Citations**:
```latex
% HOSM for arbitrary relative degree
Higher-order sliding modes \cite[Ch.~6]{Shtessel2014} handle arbitrary relative degree r by driving s, ds/dt, ..., d^(r-1)s/dt^(r-1) to zero.

% HOSM robust differentiator
HOSM arbitrary-order differentiator \cite[Ch.~6]{Shtessel2014} provides exact online differentiation in finite time.

% Chattering attenuation in HOSM
HOSM controllers \cite[Ch.~6]{Shtessel2014} achieve chattering attenuation by hiding switching in higher derivatives.
```

**Key Sections**:
- **6.1 Introduction**: Generalization from 2-SM to k-SM
- **6.2 Nested SMC Algorithm**: Recursive design
- **6.3 Quasi-Continuous HOSM**: Continuous control with switching in higher derivatives
- **6.4 Homogeneity-Based Design**: Finite-time convergence proof
- **6.5 HOSM Robust Differentiator**: Online differentiation without noise amplification
- **6.12 Notes and References** (line ~247): Historical context
- **6.13 Exercises** (line ~248): Homework problems

**Relevance to Thesis**:
- Future work: HOSM for DIP with higher relative degree
- Robust differentiator for velocity estimation (avoids noisy numerical differentiation)

---

### Chapter 7: HOSM Observers and Identification

**Used in Thesis**: Future work (advanced state estimation)

**Content Summary**:
State observation, parameter identification, and unknown input reconstruction using HOSM differentiators. Covers nonlinear system observers, parameter identification algorithms, and case studies (pendulum, satellite).

**LaTeX Citations**:
```latex
% HOSM observers
HOSM observers \cite[Ch.~7]{Shtessel2014} estimate states and identify parameters simultaneously.

% Parameter identification via HOSM
Parameter identification using HOSM \cite[Ch.~7]{Shtessel2014} provides online estimation without persistent excitation.
```

**Relevance to Thesis**:
- Future extension: Online parameter identification for DIP (masses, lengths, friction)

---

### Chapter 8: Applications and Case Studies

**Used in Thesis**: Section 7.2 (Experimental Validation - Case Studies Reference)

**Content Summary**:
Practical applications of SMC and HOSM to real-world systems including power converters, motors, aircraft/missile control, satellite formation, and robotics.

**LaTeX Citations**:
```latex
% SMC applications survey
SMC applications \cite[Ch.~8]{Shtessel2014} span power electronics, aerospace, and robotics.

% Satellite formation control via SMC
Satellite formation control \cite[Sec.~8.4]{Shtessel2014} demonstrates HOSM effectiveness for underactuated systems.
```

**Key Case Studies**:
- **8.4 Satellite Formation Control** (line ~309-316): SMDO (sliding mode disturbance observer)

**Relevance to Thesis**:
- Demonstrates SMC applicability to underactuated systems (similar to DIP)

---

## Quick Reference Table

| Content Type | Location | Thesis Section | Citation |
|--------------|----------|----------------|----------|
| SMC fundamentals | Ch. 1 | 2.3, 4.1 | `\cite[Ch.~1]{Shtessel2014}` |
| Chattering elimination | Sec. 1.2.1, 1.2.2 | 4.1, 5.2 | `\cite[Sec.~1.2]{Shtessel2014}` |
| Filippov solution | Sec. 2.1.1 | 4.3 | `\cite[Sec.~2.1.1]{Shtessel2014}` |
| Eigenvalue placement | Sec. 2.2.2 | 4.2 | `\cite[Sec.~2.2.2]{Shtessel2014}` |
| LQR sliding surface | Sec. 2.2.3 | 4.2 | `\cite[Sec.~2.2.3]{Shtessel2014}` |
| Integral sliding mode | Sec. 2.7 | Future work | `\cite[Sec.~2.7]{Shtessel2014}` |
| 2-SM theory | Ch. 4 | 4.5, 4.6 | `\cite[Ch.~4]{Shtessel2014}` |
| Super-twisting (STA) | Sec. 4.3 | 4.5 | `\cite[Sec.~4.3]{Shtessel2014}` |
| Variable-gain STA | Sec. 4.7 | 4.6 | `\cite[Sec.~4.7]{Shtessel2014}` |
| Parasitic dynamics | Ch. 5 | 5.3 | `\cite[Ch.~5]{Shtessel2014}` |
| HOSM theory | Ch. 6 | 2.3 | `\cite[Ch.~6]{Shtessel2014}` |
| HOSM observers | Ch. 7 | Future work | `\cite[Ch.~7]{Shtessel2014}` |

---

## Citation Statistics

**Total Citations in Thesis**: 0 (to be updated as thesis develops)
**Sections Referenced**: 0
**Chapters Cited**: 0

---

## Notes

### Relationship to Other Papers

**Complements Levant2007**:
- Levant2007: Original 2-SM/HOSM theory (compact journal paper)
- Shtessel2014: Comprehensive textbook treatment with examples
- Together provide theory + pedagogy

**Complements Slotine1983/1986**:
- Slotine1983: Classical SMC tracking (historical foundation)
- Shtessel2014: Modern SMC including 2-SM/HOSM (state-of-the-art)
- Together cover 1980s foundations → 2010s advances

**Complements Plestan2010**:
- Plestan2010: Adaptive gain methodology (specific algorithm)
- Shtessel2014 Sec. 4.7: Variable-gain STA (general framework)
- Together provide adaptive SMC completeness

---

### Critical for Thesis

**MUST-CITE Sections**:
1. **Chapter 1** - SMC introduction for readers unfamiliar with SMC
2. **Chapter 2, Sec. 2.2** - Sliding surface design (eigenvalue placement)
3. **Chapter 4** - Super-twisting algorithm (STA-SMC controller foundation)
4. **Chapter 4, Sec. 4.7** - Variable-gain STA (Hybrid Adaptive STA-SMC foundation)

**Optional but Valuable**:
- Chapter 5 - Robustness analysis
- Chapter 6 - HOSM (for literature review completeness)
- Chapter 8 - Applications (for context)

---

## Cross-References to Thesis Controllers

| Thesis Controller | Shtessel2014 Reference | Key Sections |
|-------------------|------------------------|--------------|
| Classical SMC | Ch. 1-2 | Sec. 1.1-1.6, 2.2-2.4 |
| STA-SMC | Ch. 4 | Sec. 4.3 |
| Adaptive SMC | Ch. 2, Sec. 2.7 + Plestan2010 | Sec. 2.7 (ISM), Plestan adaptive |
| Hybrid Adaptive STA | Ch. 4, Sec. 4.7 + Plestan2010 | Sec. 4.7 + Plestan Algorithm 2 |

---

## Important Equations

### Super-Twisting Algorithm (STA) - Chapter 4

**Standard Form**:
```
u = u₁ + u₂
u₁ = -λ₁ |s|^(1/2) sign(s)
u̇₂ = -λ₂ sign(s)
```

**Where**:
- s: sliding variable
- λ₁, λ₂: positive gains
- Requires only s measurement (NOT ds/dt!)

**Stability Condition** (sufficient):
```
λ₁ > √(2C)
λ₂ > (5C / 2λ₁)

Where C: Lipschitz constant of disturbance
```

**Finite-Time Convergence**:
- s → 0 and ds/dt → 0 in finite time T_reach
- Chattering amplitude O(T) for sampling time T (vs. O(1) for conventional SMC)

---

### Variable-Gain STA - Chapter 4, Section 4.7

**Adaptive Gain Selection**:
```
λ₁ = λ₁(s), λ₂ = λ₂(s)

Typical choice:
λ₁(s) = k₁ + k₂ |s|^p
λ₂(s) = k₃ + k₄ |s|^q

Where k₁, k₂, k₃, k₄ > 0, p, q ≥ 0
```

**Advantages**:
- No need for disturbance bound C knowledge
- Automatic adaptation to disturbance magnitude
- Reduced chattering when |s| small
- Maintains robustness when |s| large

---

## BibTeX Entry

```bibtex
@book{Shtessel2014,
  author    = {Yuri Shtessel and Christopher Edwards and Leonid Fridman and Arie Levant},
  title     = {Sliding Mode Control and Observation},
  publisher = {Springer},
  address   = {New York},
  year      = {2014},
  series    = {Control Engineering},
  isbn      = {978-0-8176-4892-3},
  doi       = {10.1007/978-0-8176-4893-0},
  note      = {Comprehensive textbook on conventional SMC, 2-SM, and HOSM with Matlab examples}
}
```

**Status**: [ ] Added to references.bib  [ ] Verified complete

---

## Checklist

### Initial Setup
- [x] PDF file location confirmed
- [x] BibTeX key assigned (Shtessel2014)
- [x] Text extracted successfully (19,064 lines)
- [x] Document structure identified (8 chapters)

### Content Extraction
- [x] Key chapters identified and summarized
- [x] Important sections located (line numbers noted)
- [x] Relevant equations documented (STA, variable-gain STA)
- [x] Cross-references to thesis controllers mapped

### Thesis Integration
- [ ] Citations added to thesis (pending)
- [ ] Tracking updated with thesis section numbers (pending)
- [x] Cross-references identified (Levant2007, Slotine1983/1986, Plestan2010)
- [ ] BibTeX entry added to references.bib (pending)

### Quality Assurance
- [x] Chapter summaries complete
- [x] Citations formatted consistently
- [ ] No duplicate citations (to verify during thesis writing)
- [ ] All references in thesis are tracked (to verify)

---

## Usage Instructions

### Requesting Content Extraction

**Common requests**:
```
"Extract super-twisting algorithm from Shtessel2014"
"Find variable-gain STA in Shtessel2014"
"Get eigenvalue placement method from Shtessel2014 Chapter 2"
"Show me ISM (integral sliding mode) from Shtessel2014"
"List all 2-SM algorithms in Shtessel2014 Chapter 4"
```

### Typical Citations

**Introductory SMC concept**:
```latex
Sliding mode control provides robustness to matched disturbances and achieves finite-time convergence \cite[Ch.~1]{Shtessel2014}.
```

**Classical SMC design**:
```latex
The sliding surface is designed via eigenvalue placement \cite[Sec.~2.2.2]{Shtessel2014} to ensure desired closed-loop dynamics.
```

**Super-twisting algorithm**:
```latex
The super-twisting algorithm \cite[Sec.~4.3]{Shtessel2014} drives the sliding variable and its derivative to zero in finite time without requiring derivative measurement.
```

**Variable-gain STA**:
```latex
Variable-gain super-twisting \cite[Sec.~4.7]{Shtessel2014} adapts control gains online based on sliding variable magnitude, eliminating the need for disturbance bound knowledge.
```

**Chattering attenuation**:
```latex
Second-order sliding modes significantly attenuate chattering compared to conventional SMC by confining switching to the second derivative \cite[Ch.~4]{Shtessel2014}.
```

---

## Open Questions

1. **Exact page numbers for STA algorithm**
   - Source: Chapter 4, Section 4.3
   - Status: [PENDING] Requires searching extracted text for section start
   - Workaround: Use chapter-level citation `\cite[Ch.~4]{Shtessel2014}` for now

2. **Variable-gain STA convergence proof**
   - Source: Chapter 4, Section 4.7 (line ~170-179)
   - Status: [READY] Can extract exact theorem from text
   - Action: Search text for "Theorem" near line 170

3. **ISM detailed design procedure**
   - Source: Chapter 2, Section 2.7 (line ~4936+)
   - Status: [READY] Can extract from text
   - Relevance: Future work for reaching-phase elimination

---

## See Also

- [Master Index](INDEX.md) - All tracked PDFs
- [AI Citation Workflow](../../docs/thesis/AI_CITATION_WORKFLOW.md) - How to use AI for citations
- `thesis/references.bib` - BibTeX database
- Levant2007_tracking.md - Original 2-SM/HOSM theory
- Slotine1983_tracking.md - Classical SMC foundations
- Plestan2010_tracking.md - Adaptive SMC methodology

---

**Status**: [TRACKED] Complete extraction from high-quality text file (19,064 lines)

**Quality**: EXCELLENT - Full text available, chapter structure clear, key sections identified with line numbers

**Recommendation**: This is a FOUNDATIONAL reference for the thesis. Cite extensively in Chapters 2 (Literature Review), 4 (SMC Design), and 5 (Results). Prioritize Chapter 1 (intro), Chapter 2 Sec. 2.2 (design), and Chapter 4 (STA).

**Last Updated**: 2025-12-07
