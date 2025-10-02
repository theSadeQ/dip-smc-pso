#!/usr/bin/env python3
"""
Generate complete ChatGPT prompt with embedded JSON data
Creates a single markdown file that can be copy-pasted to ChatGPT
"""
import json
from pathlib import Path

def main():
    # Load the 108 claims JSON
    json_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_input_108_claims.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        claims_data = json.load(f)

    # Generate the complete markdown prompt
    output_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/CHATGPT_PROMPT_100_PERCENT.md')

    markdown_content = f'''# Complete ChatGPT Prompt for 100% Citation Accuracy

**Task:** Categorize and cite 108 code claims from a control systems research project

---

## Project Context

You are helping verify citations for a **Double Inverted Pendulum Sliding Mode Control with PSO Optimization** codebase. This is a Python scientific computing project implementing:

- **Control Systems**: Sliding Mode Control (SMC), Model Predictive Control (MPC), Adaptive Control
- **Optimization**: Particle Swarm Optimization (PSO), Genetic Algorithms, Differential Evolution, BFGS, Nelder-Mead
- **Dynamics Simulation**: Nonlinear pendulum physics, numerical integrators (Runge-Kutta)
- **Analysis Tools**: Stability analysis, convergence monitoring, performance metrics

---

## Your Task

We have **108 code claims** that need citation verification. For each claim, you must:

1. **Read the actual source code** (provided in JSON below)
2. **Classify** the claim into one of three categories
3. **Find appropriate citations** for Categories A and B only
4. **Provide rationale** based on actual code content (not the description!)

---

## Classification Rules (CRITICAL)

### Category C: Pure Implementation (NO CITATION) ✅ MOST COMMON (~70%)

Mark as **Category C** if the code is:

#### Software Engineering Patterns
- Base classes, interfaces, abstract classes (`class BaseOptimizer(ABC):`)
- Factory patterns, registry patterns (`CONTROLLER_REGISTRY = {{}}`)
- Configuration classes (`@dataclass class Config:`)
- Module imports (`from .pso import PSO` in `__init__.py`)
- Property accessors (`@property def state(self):`)
- Context managers, decorators (`@contextmanager`, `@cached_property`)

#### Infrastructure Code
- Error handling, logging (`logger.info(...)`, `raise ValueError(...)`)
- Testing utilities, fixtures (`@pytest.fixture`)
- File I/O, serialization (`def to_dict(self):`, `json.dump(...)`)
- Hardware interfaces, networking (`socket.connect(...)`)
- Threading primitives (`self.lock = threading.Lock()`)
- Type hints, type checking (`from typing import Optional[float]`)

#### Simple Computations
- Variance, mean, standard deviation (`variance = np.var(data)`)
- Array operations (`x = np.zeros(n)`)
- Data transformations, filtering
- Plotting, visualization utilities (`plt.plot(...)`)

#### Library Usage (Not Implementation)
- Calling a library function (`scipy.optimize.minimize(...)`)
- Using an existing optimizer (`result = optimizer.run()`)
- Invoking pre-built algorithms

**KEY QUESTION**: Is this "glue code" that connects components or implements standard software patterns? → **Category C**

---

### Category A: Algorithmic Theory (PEER-REVIEWED PAPER) 📄 ~20%

Mark as **Category A** if the code **implements a specific algorithm** from literature:

#### Optimization Algorithms (Implementation, Not Usage)
- **Particle Swarm Optimization**: Manual velocity/position update equations
- **Differential Evolution**: Mutation, crossover, selection operators (not calling `scipy.optimize.differential_evolution`)
- **Genetic Algorithm**: Selection, crossover, mutation operators from scratch
- **BFGS/L-BFGS**: Hessian approximation updates (not calling `scipy.optimize.minimize`)
- **Nelder-Mead Simplex**: Reflection, expansion, contraction steps (not calling library)

#### Control Algorithms
- **Sliding Mode Control**: Specific sliding surface design equations
- **Super-Twisting Algorithm**: 2nd-order sliding mode dynamics implementation
- **Model Predictive Control**: Prediction horizon optimization equations

#### Numerical Methods
- **Runge-Kutta**: Butcher tableau implementation (not calling `solve_ivp`)
- **Adams-Bashforth**: Multi-step predictor-corrector from scratch
- **Recursive Least Squares**: RLS update equations for parameter estimation

**KEY TEST**: Does the code implement the algorithm equations manually? AND Does a paper exist where the title explicitly mentions this algorithm? → **Category A**

**IMPORTANT**: If code just calls `scipy.optimize.differential_evolution(...)` → **Category C** (library usage, not implementation)

---

### Category B: Foundational Concept (TEXTBOOK) 📚 ~10%

Mark as **Category B** if code **documents/explains** a control theory concept (but doesn't implement a specific algorithm):

- **Module docstrings** explaining control theory (`"""Sliding mode control achieves robustness by...`)
- **Comments** describing theoretical foundations (`# Lyapunov stability requires V̇ < 0`)
- **Stability metrics** definitions (overshoot, settling time, rise time) in documentation

**Common Textbooks to Use**:
- Control: Ogata (2010) "Modern Control Engineering"
- Nonlinear Control: Khalil (2002) "Nonlinear Systems"
- SMC: Utkin (1992) "Sliding Modes in Control and Optimization"
- Numerical: Hairer et al. (1993) "Solving Ordinary Differential Equations"
- Optimization: Nocedal & Wright (2006) "Numerical Optimization"

**KEY TEST**: Is this a docstring or comment explaining a concept (not implementing it)? → **Category B**

---

## Decision Tree

```
START → Read actual code (ignore context description)
  ↓
  Is this implementing algorithm equations manually?
  ├─ YES → Does paper title mention this algorithm?
  │        ├─ YES → **Category A** (cite paper)
  │        └─ NO → **Category C** (no citation)
  └─ NO → Is this a docstring/comment explaining theory?
           ├─ YES → **Category B** (cite textbook)
           └─ NO → **Category C** (no citation)
```

---

## Input Data: 108 Claims with Source Code

Below is the JSON array with all 108 claims. **CRITICAL**: Base your decision on the `"code"` field, NOT the `"context"` field!

```json
{json.dumps(claims_data, indent=2, ensure_ascii=False)}
```

---

## Your Output Format

Return a JSON array with exactly 108 elements in this format:

```json
[
  {{
    "claim_id": "CODE-IMPL-XXX",
    "category": "A" | "B" | "C",
    "confidence": "HIGH" | "MEDIUM" | "LOW",
    "rationale": "Based on ACTUAL CODE: brief explanation (1-2 sentences)",
    "code_summary": "What this code does (1 sentence, <50 words)",

    // IF CATEGORY A (Peer-Reviewed Paper):
    "algorithm_name": "Specific algorithm name",
    "suggested_citation": "Author (Year)",
    "bibtex_key": "author_year_keyword",
    "doi_or_url": "DOI (10.xxxx/...) or arXiv URL",
    "paper_title": "Full paper title",
    "reference_type": "journal" | "conference" | "arxiv",
    "verification": "Why this paper matches code (cite equation/section if possible)",

    // IF CATEGORY B (Textbook):
    "concept": "Control theory concept being documented",
    "suggested_citation": "Author (Year)",
    "bibtex_key": "author_year_keyword",
    "isbn": "ISBN number",
    "book_title": "Full book title",
    "reference_type": "book",
    "chapter_section": "Relevant chapter/section (if known)",

    // IF CATEGORY C (No Citation):
    // Leave citation fields empty or omit them
    "suggested_citation": "",
    "bibtex_key": "",
    "doi_or_url": "",
    "reference_type": ""
  }},
  ...
]
```

---

## Known Algorithm Citations (For Reference)

If you detect these algorithms being **implemented** (not just called), use these citations:

### Optimization Algorithms
- **Differential Evolution**: Storn & Price (1997) "Differential Evolution – A Simple and Efficient Heuristic..." DOI: 10.1023/A:1008202821328
- **Genetic Algorithm**: Goldberg (1989) "Genetic Algorithms in Search, Optimization, and Machine Learning" ISBN: 978-0201157673
- **BFGS**: Nocedal & Wright (2006) "Numerical Optimization" ISBN: 978-0387303031 (Chapter 6)
- **Nelder-Mead**: Nelder & Mead (1965) "A Simplex Method for Function Minimization" DOI: 10.1093/comjnl/7.4.308

### Numerical Methods
- **Recursive Least Squares**: Ljung (1999) "System Identification: Theory for the User" ISBN: 978-0136566953
- **Runge-Kutta (RK45)**: Hairer et al. (1993) "Solving Ordinary Differential Equations I" ISBN: 978-3540566700

### Control Theory
- **Sliding Mode Control Theory**: Utkin (1992) "Sliding Modes in Control and Optimization" ISBN: 978-3642843815
- **Control Stability Metrics**: Ogata (2010) "Modern Control Engineering" ISBN: 978-0136156734

---

## Citation Quality Requirements

### Category A Citations Must:
1. ✅ Paper title explicitly mentions the algorithm
2. ✅ DOI format is `10.xxxx/...` or arXiv URL
3. ✅ Reference type is `journal`, `conference`, or `arxiv`
4. ✅ You verified the abstract matches the implementation
5. ❌ Do NOT cite generic "optimization" papers
6. ❌ Do NOT cite Wikipedia or blog posts

### Category B Citations Must:
1. ✅ Standard textbook from graduate control/optimization courses
2. ✅ ISBN included
3. ✅ Reference type is `book`

---

## Example Outputs

### Example 1: Category C (No Citation) - Module Import

**Input Code:**
```python
from .pso import PSO
from .differential import DifferentialEvolution

__all__ = ["PSO", "DifferentialEvolution"]
```

**Output:**
```json
{{
  "claim_id": "CODE-IMPL-XXX",
  "category": "C",
  "confidence": "HIGH",
  "rationale": "Module __init__.py imports - pure Python packaging infrastructure",
  "code_summary": "Exports PSO and DifferentialEvolution classes for module interface",
  "suggested_citation": "",
  "bibtex_key": "",
  "doi_or_url": "",
  "reference_type": ""
}}
```

---

### Example 2: Category A (Algorithm Implementation) - Differential Evolution

**Input Code:**
```python
def _mutation(self, population, F):
    """Perform DE/rand/1 mutation strategy."""
    n_pop = len(population)
    mutants = []
    for i in range(n_pop):
        indices = [idx for idx in range(n_pop) if idx != i]
        r1, r2, r3 = random.sample(indices, 3)
        mutant = population[r1] + F * (population[r2] - population[r3])
        mutants.append(mutant)
    return mutants
```

**Output:**
```json
{{
  "claim_id": "CODE-IMPL-XXX",
  "category": "A",
  "confidence": "HIGH",
  "rationale": "Implements DE/rand/1 mutation operator from scratch (not calling library)",
  "code_summary": "Differential evolution mutation: v_i = x_r1 + F(x_r2 - x_r3)",
  "algorithm_name": "Differential Evolution",
  "suggested_citation": "Storn & Price (1997)",
  "bibtex_key": "storn1997differential",
  "doi_or_url": "10.1023/A:1008202821328",
  "paper_title": "Differential Evolution – A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces",
  "reference_type": "journal",
  "verification": "Paper Eq. (1) defines DE/rand/1 mutation: v_i = x_r1 + F(x_r2 - x_r3), exactly matches implementation"
}}
```

---

### Example 3: Category C (Library Usage) - NOT Implementation

**Input Code:**
```python
from scipy.optimize import differential_evolution

def optimize_gains(objective_func, bounds):
    result = differential_evolution(objective_func, bounds)
    return result.x
```

**Output:**
```json
{{
  "claim_id": "CODE-IMPL-XXX",
  "category": "C",
  "confidence": "HIGH",
  "rationale": "Calls scipy library function - NOT implementing the algorithm",
  "code_summary": "Uses scipy.optimize.differential_evolution (library call, not implementation)",
  "suggested_citation": "",
  "bibtex_key": "",
  "doi_or_url": "",
  "reference_type": ""
}}
```

---

### Example 4: Category B (Textbook Concept)

**Input Code:**
```python
"""
Stability Analysis Metrics.

Computes standard control system performance metrics:
- Settling time: Time for error to remain within ±2% of final value
- Overshoot: Maximum deviation from final value
- Rise time: Time to reach 90% of final value

These metrics characterize the transient response of control systems.
"""
```

**Output:**
```json
{{
  "claim_id": "CODE-IMPL-XXX",
  "category": "B",
  "confidence": "HIGH",
  "rationale": "Module docstring explaining standard control metrics (not implementing specific algorithm)",
  "code_summary": "Documents stability metrics definitions (settling time, overshoot, rise time)",
  "concept": "Transient response performance metrics for control systems",
  "suggested_citation": "Ogata (2010)",
  "bibtex_key": "ogata2010modern",
  "isbn": "978-0136156734",
  "book_title": "Modern Control Engineering",
  "reference_type": "book",
  "chapter_section": "Chapter 5: Transient Response Analysis"
}}
```

---

## Processing Guidelines

1. **Read code carefully** - Ignore the `context` field, focus on `code` field
2. **Default to Category C** - Most claims (~70%) are pure implementation
3. **Be strict for Category A** - Only if implementing algorithm equations manually
4. **For Category A** - Google Scholar search: "[algorithm name] original paper"
5. **For Category B** - Use recommended textbooks from list above
6. **For Category C** - No citation needed (most common!)

---

## Validation Checklist

Before submitting, verify:

- [ ] All 108 claims processed
- [ ] Each claim has `claim_id`, `category`, `confidence`, `rationale`, `code_summary`
- [ ] Category A claims have valid DOI (format `10.xxxx/...`) or arXiv URL
- [ ] Category A paper titles explicitly mention the algorithm
- [ ] Category B claims have ISBN numbers
- [ ] Category C claims have empty citation fields
- [ ] Rationales are based on ACTUAL CODE, not context descriptions
- [ ] Output is valid JSON array

---

## Expected Distribution

Based on project analysis:
- **Category C** (No citation): ~70-75 claims (65-70%)
- **Category A** (Papers): ~20-25 claims (20-23%)
- **Category B** (Textbooks): ~10-13 claims (10-12%)

If your distribution differs significantly, double-check Category C criteria - most infrastructure code needs no citation!

---

## BEGIN PROCESSING

Please process all 108 claims and return the complete JSON array. Take your time to:
1. Read the actual source code for each claim
2. Apply the decision tree strictly
3. Default to Category C when uncertain
4. Find appropriate citations only for Categories A and B

**START NOW** ↓
'''

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f'Generated ChatGPT prompt: {output_path}')
    print(f'File size: {output_path.stat().st_size / 1024:.1f} KB')
    print(f'Claims embedded: {len(claims_data)}')
    print('')
    print('USAGE INSTRUCTIONS:')
    print('1. Open the file in a text editor')
    print('2. Copy the ENTIRE contents (Ctrl+A, Ctrl+C)')
    print('3. Paste into ChatGPT')
    print('4. Wait for ChatGPT to process all 108 claims')
    print('5. Save ChatGPT response to chatgpt_output_108_citations.json')

if __name__ == '__main__':
    main()
