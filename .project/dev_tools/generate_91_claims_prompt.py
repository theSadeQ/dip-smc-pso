#!/usr/bin/env python3
"""
Generate ChatGPT prompt for remaining 91 claims
"""
import json
from pathlib import Path

# Load remaining claims
remaining_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/remaining_91_claims.json')
with open(remaining_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    remaining_claims = data['full_claims']

# Create input JSON for ChatGPT
claims_for_chatgpt = []
for claim in remaining_claims:
    claims_for_chatgpt.append({
        'claim_id': claim['id'],
        'code_summary': claim.get('context', ''),
        'file_path': claim.get('file_path', ''),
        'line_number': claim.get('line_number', ''),
        'description': claim.get('description', '')
    })

# Save input JSON
input_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_input_91_claims.json')
with open(input_path, 'w', encoding='utf-8') as f:
    json.dump(claims_for_chatgpt, f, indent=2)

print(f"Saved {len(claims_for_chatgpt)} claims to: {input_path}")

# Generate the ChatGPT prompt
prompt = f"""# Task: Classify 91 Code Implementation Claims

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

Classify each of the {len(claims_for_chatgpt)} claims below and provide citations for Categories A and B.

### Output Format (JSON array)

For each claim, return:

```json
{{
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
}}
```

## Citation Quality Standards

### Category A - Use ONLY these canonical references:

**Numerical Integration:**
- Euler method → Hairer et al. (1993) "Solving Ordinary Differential Equations I"
- RK4/RK45 → Hairer et al. (1993) "Solving Ordinary Differential Equations I"

**Optimization:**
- PSO → Kennedy & Eberhart (1995) DOI: 10.1109/ICNN.1995.488968
- Differential Evolution → Storn & Price (1997) DOI: 10.1023/A:1008202821328
- Nelder-Mead → Nelder & Mead (1965) DOI: 10.1093/comjnl/7.4.308
- BFGS → Nocedal & Wright (2006) "Numerical Optimization"
- Pareto optimization → Deb (2001) "Multi-Objective Optimization using Evolutionary Algorithms"
- Weighted sum → Marler & Arora (2004) DOI: 10.1007/s00158-004-0370-0

**Parameter Estimation:**
- RLS (Recursive Least Squares) → Ljung (1999) "System Identification: Theory for the User"
- Kalman Filter → Kalman (1960) DOI: 10.1115/1.3662552

**Sliding Mode Control:**
- SMC general → Utkin (1977) DOI: 10.1109/TAC.1977.1101446
- Super-Twisting → Levant (1993) DOI: 10.1016/0005-1098(93)90127-K
- Equivalent control → Utkin (1992) "Sliding Modes in Control and Optimization"
- Adaptive SMC → Slotine & Li (1991) "Applied Nonlinear Control"

### Category B - Use standard textbooks:

**Control Theory Concepts:**
- Chattering → Utkin (1992) "Sliding Modes in Control and Optimization"
- Robustness → Zhou & Doyle (1998) "Essentials of Robust Control"
- Stability → Khalil (2002) "Nonlinear Systems"
- LQR theory → Anderson & Moore (2007) "Optimal Control: Linear Quadratic Methods"
- Controllability/Observability → Ogata (2010) "Modern Control Engineering"

## Input Claims

```json
{json.dumps(claims_for_chatgpt, indent=2)}
```

## Instructions

1. Read each claim's code_summary, file_path, and description
2. Classify into Category A, B, or C
3. For A/B: provide complete citation information from canonical references above
4. For C: explain why no citation is needed
5. Return a valid JSON array with all {len(claims_for_chatgpt)} claims classified
6. Ensure 100% completion - every claim must be included in output

**CRITICAL**: Return ONLY the JSON array. No markdown, no explanations, just the JSON starting with `[` and ending with `]`.
"""

# Save prompt
prompt_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/CHATGPT_PROMPT_91_CLAIMS.md')
with open(prompt_path, 'w', encoding='utf-8') as f:
    f.write(prompt)

print(f"Saved ChatGPT prompt to: {prompt_path}")
print()
print("=" * 80)
print("PROMPT READY FOR CHATGPT")
print("=" * 80)
print()
print(f"Total claims: {len(claims_for_chatgpt)}")
print(f"Prompt length: {len(prompt):,} characters")
print()
print("Next steps:")
print("1. Open the prompt file and copy the entire content")
print("2. Paste into ChatGPT (GPT-4 or Claude)")
print("3. Save response as: chatgpt_output_91_citations.json")
print("4. Run: python .dev_tools/apply_chatgpt_citations.py")
