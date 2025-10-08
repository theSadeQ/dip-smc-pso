# Formal Theorem Citation Prompts

This directory contains 11 comprehensive, self-contained prompts for finding academic citations for theoretical claims in the DIP-SMC-PSO project.

## Overview

Each prompt is designed to be copied directly into any AI tool (Claude, ChatGPT, Perplexity, Deep Research, etc.) without requiring any file uploads or additional context.

**Total prompts:** 11 (covering 17 claim instances - some theorems appear in multiple topics)

**Estimated cost:** $0.35 - $1.00 total (if using paid AI services)

**Estimated time:** 30-60 minutes to process all prompts and review results

---

## Prompt Index

### Fault Detection & Isolation (1 prompt)

**[PROMPT_01: Fault Detection Hysteresis](PROMPT_01_Fault_Detection_Hysteresis.md)**
- **Theorem:** Hysteresis with deadband prevents oscillation
- **Domain:** FDI systems, threshold logic
- **Key topics:** Residual evaluation, chattering prevention

---

### PSO Optimization Theory (4 prompts)

**[PROMPT_02: PSO Global Asymptotic Stability](PROMPT_02_PSO_Global_Asymptotic_Stability.md)**
- **Theorem:** PSO-optimized gains ensure global asymptotic stability
- **Domain:** Controller gain tuning, stability theory
- **Key topics:** Lyapunov stability, underactuated systems

**[PROMPT_03: PSO Lyapunov Stability Maintenance](PROMPT_03_PSO_Lyapunov_Stability.md)**
- **Theorem:** PSO-optimized gains maintain Lyapunov stability
- **Domain:** Constrained optimization, closed-loop systems
- **Key topics:** Stability preservation, robust optimization

**[PROMPT_04: PSO Particle Convergence](PROMPT_04_PSO_Particle_Convergence.md)**
- **Theorem:** Particle converges to stable trajectory under conditions
- **Domain:** PSO algorithm theory
- **Key topics:** Parameter stability, convergence analysis

**[PROMPT_05: PSO Global Convergence (Unimodal)](PROMPT_05_PSO_Global_Convergence_Unimodal.md)**
- **Theorem:** PSO converges to global optimum (probability 1) for unimodal functions
- **Domain:** Stochastic optimization
- **Key topics:** Almost sure convergence, decreasing inertia

---

### Sliding Mode Control Theory (6 prompts)

**[PROMPT_06: Sliding Surface Exponential Stability](PROMPT_06_Sliding_Surface_Exponential_Stability.md)**
- **Theorem:** Positive sliding parameters ensure exponential stability
- **Domain:** Sliding surface design
- **Key topics:** Hurwitz stability, convergence rates

**[PROMPT_07: SMC Reaching Condition (Finite-Time)](PROMPT_07_SMC_Reaching_Condition_Finite_Time.md)**
- **Theorem:** Reaching condition ensures finite-time convergence
- **Domain:** Reaching phase analysis
- **Key topics:** Lyapunov reaching law, time bounds

**[PROMPT_08: Classical SMC Global Finite-Time](PROMPT_08_Classical_SMC_Global_Finite_Time.md)**
- **Theorem:** Classical SMC with η > ρ ensures global finite-time convergence
- **Domain:** Robust control, uncertainty bounds
- **Key topics:** Switching gain selection, matched disturbances

**[PROMPT_09: Super-Twisting Algorithm](PROMPT_09_Super_Twisting_Algorithm_Finite_Time.md)**
- **Theorem:** STA ensures finite-time convergence to {s=0, ṡ=0}
- **Domain:** Second-order sliding modes
- **Key topics:** Chattering reduction, continuous control

**[PROMPT_10: Adaptive SMC Control Law](PROMPT_10_Adaptive_SMC_Control_Law.md)**
- **Theorem:** Adaptive law ensures stability and bounded adaptation
- **Domain:** Adaptive control
- **Key topics:** Online gain tuning, Lyapunov adaptation

**[PROMPT_11: Boundary Layer Tracking Error](PROMPT_11_Boundary_Layer_Tracking_Error_Bound.md)**
- **Theorem:** Boundary layer method gives ultimately bounded tracking error
- **Domain:** Chattering elimination
- **Key topics:** Continuous approximation, trade-off analysis

---

## How to Use

### For Each Prompt:

1. **Open the prompt file** (e.g., `PROMPT_01_Fault_Detection_Hysteresis.md`)
2. **Copy entire content** (Ctrl+A, Ctrl+C)
3. **Paste into AI tool** (Claude, ChatGPT, Perplexity, etc.)
4. **Review citations** provided by AI
5. **Save relevant citations** to your documentation

### Recommended AI Tools:

| Tool | Best For | Cost | Notes |
|------|----------|------|-------|
| **Claude** | Deep technical analysis | ~$0.03/prompt | Best for complex theorems |
| **ChatGPT** | Quick citations | ~$0.02/prompt | Fast, good coverage |
| **Perplexity Pro** | Latest papers | Subscription | Real-time search included |
| **Deep Research** | Comprehensive surveys | ~$2/prompt | Overkill for single theorems |
| **Google Scholar** | Free manual search | Free | Time-consuming |

---

## Expected Output Format

Each AI response should provide:

1. **2-3 authoritative citations**
2. **Full bibliographic information** (authors, title, venue, year, pages)
3. **DOI or URL** for each citation
4. **Relevance explanation** (2-3 sentences per citation)
5. **Key theorem/equation reference** from the cited work

---

## Claim Coverage

| Claim ID | Topics | Prompt File |
|----------|--------|-------------|
| FORMAL-THEOREM-001 | Fault Detection | PROMPT_01 |
| FORMAL-THEOREM-004 | PSO Optimization, Lyapunov, Inverted Pendulum | PROMPT_02 |
| FORMAL-THEOREM-005 | PSO Optimization, Control Theory, Lyapunov | PROMPT_03 |
| FORMAL-THEOREM-008 | Control Theory, PSO | PROMPT_04 |
| FORMAL-THEOREM-010 | PSO Optimization | PROMPT_05 |
| FORMAL-THEOREM-016 | Sliding Mode Classical | PROMPT_06 |
| FORMAL-THEOREM-019 | Sliding Mode Classical | PROMPT_07 |
| FORMAL-THEOREM-020 | Sliding Mode Classical, Super-Twisting | PROMPT_08 |
| FORMAL-THEOREM-021 | Super-Twisting | PROMPT_09 |
| FORMAL-THEOREM-022 | Control Theory, Adaptive SMC | PROMPT_10 |
| FORMAL-THEOREM-023 | Sliding Mode Classical, Boundary Layer | PROMPT_11 |

---

## Quality Standards

Each prompt ensures:

✅ **Self-contained** - No file requests, no follow-up questions needed
✅ **Comprehensive context** - Full mathematical and domain background
✅ **Specific requirements** - Clear citation criteria
✅ **Authoritative focus** - Targets seminal papers and classic textbooks
✅ **Structured output** - Specifies exact format for AI response

---

## Next Steps After Citation Collection

1. **Review citations** for relevance and authority
2. **Create BibTeX entries** for accepted citations
3. **Update documentation** with proper citations
4. **Verify DOI links** are accessible
5. **Check for duplicate citations** across multiple theorems

---

## Notes

- Some theorems (FORMAL-THEOREM-004, 005, 020) appear in multiple topics - this is expected
- The 11 unique prompts cover all 17 claim instances
- Each prompt is optimized for academic rigor, not just keyword matching
- Prompts include historical context and seminal author names to guide AI

---

**Total theoretical claims:** 17 instances → **11 unique theorems** → **11 self-contained prompts**

**Ready to use immediately - just copy, paste, and collect citations!**
