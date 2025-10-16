# Task: Classify 9 Code Implementation Claims - Subgroup 1/10

**Subgroup**: SMC Algorithms - Adaptive & Hybrid
**Focus**: Adaptive parameter estimation (RLS), hybrid switching logic

You are a research assistant helping classify code implementation claims for a control systems research paper on Double Inverted Pendulum with Sliding Mode Control and PSO Optimization.

## Classification Categories

**Category A - Algorithm Implementation (needs peer-reviewed paper)**
- Implements a specific algorithm (e.g., RLS, Euler, RK4, PSO, Kalman Filter, Super-Twisting)
- Requires citation to the original algorithm paper or canonical reference
- Example: "Implements Recursive Least Squares parameter estimation"

**Category B - Theoretical Concept (needs textbook)**
- Discusses a control theory concept without implementing an algorithm
- Requires citation to a standard textbook
- Example: "Documentation explaining chattering phenomenon in SMC"

**Category C - Pure Implementation (NO citation needed)**
- Pure software implementation: initialization, validation, factory methods, getters/setters
- Infrastructure code: interfaces, abstract classes, type checking
- Example: "Initialize controller state variables"

## Your Task

Classify each of the 9 claims below and provide citations for Categories A and B.

### Output Format (JSON array)

For each claim, return:

```json
{
  "claim_id": "CODE-IMPL-XXX",
  "category": "A" | "B" | "C",
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "rationale": "Brief explanation of category choice",
  "code_summary": "One-line summary of what the code does",
  "needs_citation": true | false,

  // For Category A (algorithm paper):
  "algorithm_name": "Full algorithm name",
  "suggested_citation": "Author(s) (Year)",
  "bibtex_key": "authorYYYYkeyword",
  "doi_or_url": "10.xxxx/yyyy or arXiv:xxxx.xxxxx",
  "paper_title": "Full Paper Title",
  "reference_type": "paper",

  // For Category B (textbook):
  "concept": "Control theory concept name",
  "suggested_citation": "Author(s) (Year)",
  "bibtex_key": "authorYYYYkeyword",
  "isbn": "ISBN number",
  "book_title": "Full Book Title",
  "reference_type": "book",
  "chapter_section": "Chapter X: Title",

  // For Category C (omit citation fields):
  "implementation_type": "initialization|validation|interface|factory|utility"
}
```

## Citation Quality Standards

### Category A - Use ONLY these canonical references:

**Numerical Integration:**
- Euler method → Hairer et al. (1993) "Solving Ordinary Differential Equations I" (ISBN: 978-3540566700)
- RK4/RK45 → Hairer et al. (1993) "Solving Ordinary Differential Equations I" (ISBN: 978-3540566700)

**Optimization:**
- PSO → Kennedy & Eberhart (1995) DOI: 10.1109/ICNN.1995.488968
- Differential Evolution → Storn & Price (1997) DOI: 10.1023/A:1008202821328
- Nelder-Mead → Nelder & Mead (1965) DOI: 10.1093/comjnl/7.4.308
- BFGS → Nocedal & Wright (2006) "Numerical Optimization" (ISBN: 978-0387303031)
- Pareto optimization → Deb (2001) "Multi-Objective Optimization using Evolutionary Algorithms" (ISBN: 978-0471873396)
- Weighted sum → Marler & Arora (2004) DOI: 10.1007/s00158-004-0370-0

**Parameter Estimation:**
- RLS (Recursive Least Squares) → Ljung (1999) "System Identification: Theory for the User" (ISBN: 978-0136566953)
- Kalman Filter → Kalman (1960) DOI: 10.1115/1.3662552

**Sliding Mode Control:**
- SMC general → Utkin (1977) DOI: 10.1109/TAC.1977.1101446
- Super-Twisting → Levant (1993) DOI: 10.1016/0005-1098(93)90127-K
- Equivalent control → Utkin (1992) "Sliding Modes in Control and Optimization" (ISBN: 978-3642843976)
- Adaptive SMC → Slotine & Li (1991) "Applied Nonlinear Control" (ISBN: 978-0130408907)
- Hybrid switching → Branicky (1998) DOI: 10.1109/9.664150

### Category B - Use standard textbooks:

**Control Theory Concepts:**
- Chattering → Utkin (1992) "Sliding Modes in Control and Optimization" (ISBN: 978-3642843976)
- Robustness → Zhou & Doyle (1998) "Essentials of Robust Control" (ISBN: 978-0135258330)
- Stability → Khalil (2002) "Nonlinear Systems" (ISBN: 978-0130673893)
- LQR theory → Anderson & Moore (2007) "Optimal Control: Linear Quadratic Methods" (ISBN: 978-0486457666)
- Controllability/Observability → Ogata (2010) "Modern Control Engineering" (ISBN: 978-0136156734)

## Input Claims

```json
[
  {
    "claim_id": "CODE-IMPL-132",
    "code_summary": "Implements online estimation of system uncertainties and disturbance bounds...",
    "file_path": "src\\controllers\\smc\\algorithms\\adaptive\\parameter_estimation.py",
    "line_number": "1",
    "description": "online estimation (attributed to: system uncertainties and disturbance bounds)"
  },
  {
    "claim_id": "CODE-IMPL-135",
    "code_summary": "Update parameter estimates using RLS algorithm...",
    "file_path": "src\\controllers\\smc\\algorithms\\adaptive\\parameter_estimation.py",
    "line_number": "250",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-150",
    "code_summary": "Initialize individual SMC controllers based on hybrid mode...",
    "file_path": "src\\controllers\\smc\\algorithms\\hybrid\\controller.py",
    "line_number": "112",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-152",
    "code_summary": "Hybrid Switching Logic for Multi-Controller SMC...",
    "file_path": "src\\controllers\\smc\\algorithms\\hybrid\\switching_logic.py",
    "line_number": "1",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-155",
    "code_summary": "Evaluate switching based on control effort...",
    "file_path": "src\\controllers\\smc\\algorithms\\hybrid\\switching_logic.py",
    "line_number": "265",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-157",
    "code_summary": "Evaluate switching based on adaptation rate (for adaptive controllers)...",
    "file_path": "src\\controllers\\smc\\algorithms\\hybrid\\switching_logic.py",
    "line_number": "319",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-159",
    "code_summary": "Evaluate switching based on time (round-robin or scheduled switching)...",
    "file_path": "src\\controllers\\smc\\algorithms\\hybrid\\switching_logic.py",
    "line_number": "381",
    "description": "None (attributed to: None)"
  },
  {
    "claim_id": "CODE-IMPL-121",
    "code_summary": "use named tuples are\n    subclasses of ``tuple``...",
    "file_path": "src\\controllers\\smc\\adaptive_smc.py",
    "line_number": "263",
    "description": "named tuples are\n    subclasses (attributed to: ``tuple``)"
  },
  {
    "claim_id": "CODE-IMPL-122",
    "code_summary": "Set dynamics model (for compatibility, not used in this implementation)...",
    "file_path": "src\\controllers\\smc\\adaptive_smc.py",
    "line_number": "427",
    "description": "None (attributed to: None)"
  }
]
```

## Instructions

1. Read each claim's code_summary, file_path, and description
2. Classify into Category A, B, or C
3. For A/B: provide complete citation information from canonical references above
4. For C: explain why no citation is needed
5. Return a valid JSON array with all 9 claims classified
6. Ensure 100% completion - every claim must be included in output

**CRITICAL**: Return ONLY the JSON array. No markdown, no explanations, just the JSON starting with `[` and ending with `]`.
