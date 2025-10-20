# LaTeX Integration Checklist
## Chapter 6 (Experimental Setup)

**Date**: 2025-10-20
**Document**: `section_VI_experimental_setup.md`
**Purpose**: Pre-submission checklist for LaTeX conversion
**Status**: ✅ **READY FOR LaTeX INTEGRATION**

---

## 1. Equation Blocks

### Inline Math ($ ... $)
**Status**: ✅ All inline math uses correct LaTeX syntax
**Examples**:
- `$\Delta t = 0.001$` (line 12)
- `$\theta_1(0), \theta_2(0)$` (line 39)
- `$u[k] = u_{\text{eq}}[k] + u_{\text{sw}}[k]$` (line 61)

**Action Required**: ✅ None (already correct)

### Display Math (```latex ... ```)
**Status**: ✅ All display blocks use correct code fence format
**Count**: 15+ display equations
**Examples**:
- RK4 timestep (line 11-13)
- Simulation duration (line 24-26)
- Step disturbance (line 95-100)
- Cohen's d formula (line 291-293)

**Action Required for LaTeX**: Convert to `\begin{equation}...\end{equation}` or `\[...\]` format

**Conversion Script** (recommended):
```python
# Replace ```latex ... ``` with LaTeX display math
import re
text = open('section_VI_experimental_setup.md').read()
text = re.sub(r'```latex\n(.*?)\n```', r'\\[\n\\1\n\\]', text, flags=re.DOTALL)
```

---

## 2. Citation Placeholders

### Current Status
**Citations Needed**: 8-12 references (estimated)
**Current State**: ❌ No citation markers in text

### Recommended Citations

#### Numerical Methods
| Location | Citation Needed | Suggested Reference |
|----------|----------------|---------------------|
| Line 9 | RK4 method | Press et al. (2007) Numerical Recipes |
| Line 19 | Comparison to ODE45 | Shampine & Reichelt (1997) MATLAB ODE Suite |

#### Statistical Methods
| Location | Citation Needed | Suggested Reference |
|----------|----------------|---------------------|
| Line 275 | Welch's t-test | Welch (1947) Biometrika |
| Line 289 | Cohen's d | Cohen (1988) Statistical Power Analysis |
| Line 313 | Bootstrap CI | Efron & Tibshirani (1993) An Introduction to the Bootstrap |
| Line 330 | Bonferroni correction | Bonferroni (1936) OR Dunn (1961) |

#### Control Theory
| Location | Citation Needed | Suggested Reference |
|----------|----------------|---------------------|
| Line 58 | SMC equivalent control | Slotine & Li (1991) Applied Nonlinear Control |
| Line 68 | Sliding surface derivative | Utkin et al. (2009) Sliding Mode Control |

#### PSO Optimization
| Location | Citation Needed | Suggested Reference |
|----------|----------------|---------------------|
| Line 146 | PSO algorithm | Kennedy & Eberhart (1995) OR Poli et al. (2007) |
| Line 146 | PySwarms library | Miranda (2018) Journal of Open Source Software |

### Action Required
**Before Submission**: Insert `\cite{...}` markers at appropriate locations

**Example**:
```latex
The nonlinear DIP dynamics (Section III) are integrated using the
4th-order Runge-Kutta (RK4) method\cite{Press2007} with fixed time step...
```

---

## 3. Figure Captions

### Main Chapter Figures
**Status**: ✅ N/A (Chapter 6 has no main-text figures, all results in Chapter 7)

### Appendix Figures
**Status**: ✅ **COMPLETE** - LaTeX captions file created

**File**: `.artifacts/LT7_research_paper/figures/figure_captions_appendix.tex`

**Contents**:
- Figure A-1: Normality validation (Q-Q plots)
- Figure A-2: Bootstrap convergence
- Figure A-3: Sensitivity analysis

**Labels**:
- `\label{fig:appendix-normality-validation}`
- `\label{fig:appendix-bootstrap-convergence}`
- `\label{fig:appendix-sensitivity-analysis}`

**Cross-References in Text**:
- Line 287: "see Online Appendix Figure A-1" → Replace with `\ref{fig:appendix-normality-validation}`
- Line 328: "see Online Appendix Figure A-2" → Replace with `\ref{fig:appendix-bootstrap-convergence}`
- Line 350: "see Online Appendix Figure A-3" → Replace with `\ref{fig:appendix-sensitivity-analysis}`

**Action Required for LaTeX**:
```latex
% In main text (line 287):
(see Online Appendix Figure~\ref{fig:appendix-normality-validation} for detailed normality validation)

% In main text (line 328):
(see Online Appendix Figure~\ref{fig:appendix-bootstrap-convergence} for bootstrap convergence validation)

% In main text (line 350):
(see Online Appendix Figure~\ref{fig:appendix-sensitivity-analysis} for comprehensive sensitivity analysis)
```

---

## 4. Table Formatting

### Table II: Monte Carlo Sample Sizes
**Location**: Line 141-150
**Current Format**: Markdown table
**Status**: ✅ Ready for conversion

**LaTeX Conversion**:
```latex
\begin{table}[htbp]
\centering
\caption{Monte Carlo sample sizes per experiment}
\label{tab:monte-carlo-sample-sizes}
\begin{tabular}{llll}
\toprule
Experiment & Description & Sample Size & Random Seeds \\
\midrule
MT-5 & Baseline controller comparison & 100 per controller (400 total) & 42 \\
MT-6 Training & PSO optimization (fitness evaluation) & $\sim$500 (30 particles $\times$ $\sim$17 iterations) & 42 (PSO init) \\
MT-6 Fixed & Fixed boundary layer validation & 100 & 42 \\
MT-6 Adaptive & Adaptive boundary layer validation & 100 & 42 \\
MT-7 & Robustness stress testing & 500 (50 per seed) & 42-51 (10 seeds) \\
MT-8 & Disturbance rejection & 12 (3 disturbances $\times$ 4 controllers) & N/A (deterministic) \\
\bottomrule
\end{tabular}
\end{table}
```

**Footnote [2]**: Convert to `\footnote{...}` or table note

---

## 5. Special Characters & Symbols

### Greek Letters
**Status**: ✅ All correctly escaped with LaTeX commands
**Examples**: `\theta_1`, `\theta_2`, `\alpha`, `\beta`, `\epsilon`, `\sigma`, `\Delta`

### Mathematical Operators
**Status**: ✅ Correctly formatted
**Examples**: `\times`, `\approx`, `\leq`, `\geq`, `\sim`, `\mathcal{U}`, `\mathcal{O}`

### Units
**Status**: ⚠️ Some inconsistencies

**Current**: `\, \text{s}`, `\, \text{N}`, `\, \text{rad}`
**Recommended**: Use `\unit{...}` from `siunitx` package for consistency

**Action Required**:
```latex
% Instead of:
$\Delta t = 0.001 \, \text{s}$

% Use:
$\Delta t = \SI{0.001}{\second}$
% OR
$\Delta t = 0.001~\text{s}$  % with non-breaking space
```

---

## 6. Section Headings

### Current Format
**Markdown**: `## A. Simulation Environment` (level 2)
**Markdown**: `### 1) Numerical Integration` (level 3)

### LaTeX Conversion
```latex
\section{Experimental Setup}  % VI.
\subsection{Simulation Environment}  % A.
\subsubsection{Numerical Integration}  % 1)
```

**Status**: ✅ Hierarchy clear, straightforward conversion

---

## 7. Footnotes

### Existing Footnotes
| Line | Marker | Content | Status |
|------|--------|---------|--------|
| 146 | [2] | PSO iteration convergence note | ✅ Ready |
| 307 | [1] | Cohen's d calculation note | ✅ Ready |

**LaTeX Conversion**:
```latex
% Footnote [1] (line 307):
For our MT-6 results, $d = 5.29$ indicates a very large effect\footnote{%
The reported Cohen's d = 5.29 uses a sample-weighted pooled standard deviation
formula that accounts for the different variances between fixed ($\sigma = 1.20$)
and adaptive ($\sigma = 0.13$) conditions. The traditional pooled std formula
yields $d = 4.96$. Both values far exceed the threshold for ``large effect''
($d \geq 0.8$), confirming the exceptional magnitude of chattering reduction
regardless of formula choice.}

% Footnote [2] (line 146):
MT-6 Training & PSO optimization & $\sim$500 (30 particles $\times$ $\sim$17 iterations\footnote{%
PSO was configured for a maximum of 30 iterations (as described in Chapter V),
but converged early at iteration 17 via stagnation detection (5 consecutive
iterations with fitness improvement $<0.1\%$). Early termination saved
$\sim$390 fitness evaluations (13 iterations $\times$ 30 particles) while
maintaining optimization quality.}) & 42 (PSO init) \\
```

---

## 8. Code Blocks

### Current Format
**Markdown code fences**: Used for LaTeX math only
**Status**: ✅ No actual code blocks (only math displays)

**Action Required**: Convert all ` ```latex ... ``` ` to proper LaTeX display math

---

## 9. Bold/Italic Formatting

### Bold Text
**Current**: `**Bold**` (Markdown)
**LaTeX**: `\textbf{Bold}`

**Examples**:
- Line 15: `**Integration Accuracy:**` → `\textbf{Integration Accuracy:}`
- Line 274: `**Test Statistic:**` → `\textbf{Test Statistic:}`

**Status**: ⚠️ ~40 instances to convert

### Italic Text
**Current**: None used (emphasis via bold only)
**Status**: ✅ N/A

---

## 10. Hyperlinks

### External Links
| Line | Link | Target | Status |
|------|------|--------|--------|
| 420 | GitHub repository | https://github.com/theSadeQ/dip-smc-pso | ✅ Ready |

**LaTeX Conversion**:
```latex
% Use hyperref package
Simulation source code at \url{https://github.com/theSadeQ/dip-smc-pso} (MIT License)
```

---

## 11. Conversion Checklist

### Pre-Conversion Tasks
- [✅] Verify all equations use correct LaTeX syntax
- [✅] Create figure captions file (`figure_captions_appendix.tex`)
- [✅] Validate cross-references (see `CROSS_REFERENCE_VALIDATION_REPORT.md`)
- [❌] Insert citation placeholders (⏸️ Pending bibliography)
- [✅] Check special characters (Greek, math symbols)

### Conversion Tasks
- [⏸️] Convert ` ```latex ... ``` ` to `\[...\]` or `\begin{equation}...\end{equation}`
- [⏸️] Convert `**bold**` to `\textbf{bold}`
- [⏸️] Convert markdown headings to `\section`, `\subsection`, `\subsubsection`
- [⏸️] Convert Table II to LaTeX tabular format
- [⏸️] Convert footnotes `[1]`, `[2]` to `\footnote{...}`
- [⏸️] Replace figure reference text with `\ref{...}` commands
- [⏸️] Convert GitHub URL to `\url{...}`

### Post-Conversion Verification
- [⏸️] Compile LaTeX document (check for errors)
- [⏸️] Verify all cross-references resolve
- [⏸️] Check figure/table numbering
- [⏸️] Proofread converted document

---

## 12. LaTeX Packages Required

### Recommended Packages
```latex
\usepackage{amsmath}       % Advanced math
\usepackage{amssymb}       % Math symbols
\usepackage{siunitx}       % SI units (optional but recommended)
\usepackage{booktabs}      % Professional tables (\toprule, \midrule, \bottomrule)
\usepackage{graphicx}      % Figure inclusion
\usepackage{hyperref}      % Hyperlinks and cross-references
\usepackage{cleveref}      % Smart cross-references (e.g., "Figure~\ref{...}" auto)
```

---

## 13. Final Assessment

**LaTeX Readiness**: ✅ **95% READY**

**Complete**:
- ✅ Equation syntax correct (all LaTeX-compatible)
- ✅ Figure captions prepared (appendix figures)
- ✅ Cross-references validated
- ✅ Table structure clear
- ✅ Footnotes identified

**Pending** (low-priority, easy fixes):
- ⏸️ Citation placeholders (need bibliography file)
- ⏸️ Markdown-to-LaTeX syntax conversion (automated)
- ⏸️ Units standardization (siunitx, optional)

**Estimated Conversion Time**: 1-2 hours (mostly automated find-replace)

---

**Checklist Generated**: 2025-10-20
**For**: Chapter 6 (Experimental Setup) LaTeX integration
**Status**: ✅ **PUBLICATION-READY** (pending citation insertion + mechanical conversion)
