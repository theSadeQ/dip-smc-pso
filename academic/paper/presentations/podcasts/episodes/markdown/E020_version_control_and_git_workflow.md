# E020: Version Control and Git Workflow

**Part:** Part4 Professional
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Comprehensive Presentation

---

## Overview

This episode covers version control and git workflow from the DIP-SMC-PSO project.

## Intentional Architectural Patterns

**DO NOT "FIX" These Patterns -- They Are Intentional:**

        - **Compatibility Layers**
        
            - `src/optimizer/` → `src/optimization/`
            - Backward compatibility for old imports
            - \textit{Reason:} Smooth migration, no breaking changes

        - **Re-export Chains**
        
            - `simulation\_context.py` in 3 locations
            - Import path flexibility
            - \textit{Reason:} User convenience, multiple valid import styles

        - **Model Variants**
        
            - 8 dynamics files (simplified, full, low-rank, etc.)
            - Different accuracy/performance tradeoffs
            - \textit{Reason:} Speed vs. accuracy based on use case

        - **Framework Files in `src/**`
        
            - `src/interfaces/hil/test\_automation.py` is PRODUCTION code
            - Automation framework, not pytest tests
            - \textit{Reason:} Exported in `\_\_init\_\_.py`, imported by production code

---

## Directory Placement Rules

**File Classification Decision Tree:**

    [Visual diagram - see PDF]

---

## Quality Gates (ENFORCE STRICTLY)

**Production Readiness Criteria:**

    \begin{tabular}{llc}
        \toprule
        **Gate** & **Threshold** & **Current** \\
        \midrule
        Critical issues & 0 & [OK] \\
        High-priority issues & ≤3 & [OK] \\
        Test pass rate & 100\
        Root visible items & ≤19 & [OK] (14) \\
        Malformed file names & 0 & [OK] \\
        \midrule
        Code coverage (overall) & ≥85\
        Coverage (critical) & ≥95\
        Production score & ≥70/100 & \statuserror (23.9) \\
        \bottomrule
    \end{tabular}

        **Research-Ready:** [OK] Single/multi-threaded operation validated \\
        **NOT Production-Ready:** \statuserror Quality gates 1/8 passing (score: 23.9/100)

    \textit{See:} `.ai\_workspace/guides/phase4\_status.md`

---

## File Naming Conventions

**NEVER Create These Patterns:**

            - **Braces/spaces:** `\{dir\`/}, `my folder/`
            - **Windows device names:** `nul`, `con`, `prn`, `aux`
            - **Unicode paths on Windows:** Use ASCII only
            - **Trailing dots/spaces:** `file. `, `dir.`

    **Recommended Patterns:**
    
        - **Python modules:** `snake\_case.py`
        - **Classes:** `PascalCase`
        - **Functions/variables:** `snake\_case`
        - **Constants:** `UPPER\_SNAKE\_CASE`
        - **Directories:** `lowercase\_underscores/`
        - **Scripts:** `verb\_noun.sh` (e.g., `run\_tests.sh`)

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
