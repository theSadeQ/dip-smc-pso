# Batch Filtering Guide - Quick Reference

**Last Updated:** 2025-10-03
**System:** Citation Research Batch Generation v2.0

---

## TL;DR

✅ **Filtering is now automatic** - Claims are pre-filtered during batch generation
✅ **Batch 12 is 100% invalid** - Skip it (see `SKIP_NOTICE.md`)
✅ **Use enhanced prompts** - "IMPORTANT - Citation Scope" section guides ChatGPT

---

## What Changed?

### Before Optimization
- All claims included in batches (valid + invalid)
- Wasted time on software patterns
- ChatGPT confused about what needs citations

### After Optimization
- **Pre-filtering**: Invalid claims removed before batch creation
- **Smart prompts**: Clear DO/DON'T guidance for ChatGPT
- **Skip notices**: Invalid batches marked for skipping

---

## How to Use

### 1. Check for Skip Notices

Before starting ANY batch:

```bash
ls artifacts/research_batches/[batch_id]/SKIP_NOTICE.md
```

**If file exists:** Skip this batch entirely (no valid claims)
**If file doesn't exist:** Proceed normally

### 2. Use Enhanced Prompts

All regenerated prompts now include:

```markdown
**IMPORTANT - Citation Scope (Read First!):**

✅ DO provide citations for:
- Mathematical theorems
- Control theory algorithms
- Statistical methods (theory)
- Numerical analysis techniques (algorithms)

❌ DO NOT provide citations for:
- Software design patterns
- Module/package organization
- Implementation wrappers
- Generic software architecture
```

**Result:** ChatGPT responds with either:
- Valid citation (5 fields)
- "SKIP: Standard software engineering pattern - no citation needed"

### 3. Regenerate Old Batches (Optional)

To apply filtering to existing batches:

```bash
cd D:\Projects\main
python artifacts/research_batches/_AUTOMATION/generate_batch_folders.py
```

This will:
- Apply `_should_skip_claim()` filter
- Generate skip notices for invalid batches
- Create enhanced prompts for valid batches

---

## Filter Logic

### Claims That Get SKIPPED

**Malformed Claims:**
- "None (attributed to: None)"
- "Returns (attributed to: ...)"
- Descriptions < 10 characters
- Word count < 3 words

**Software Patterns:**
- Factory/Strategy/Observer patterns
- "Statistical analysis package" (organization, not theory)
- "Benchmarking tools" (utilities, not algorithms)
- "Enterprise Controller Factory" (design pattern)

**Implementation Details:**
- "implements statistical methods" (code, not theory)
- "vectorised tuner" (optimization, not algorithm)
- "high-throughput" (performance detail)

**Generic Descriptions:**
- Single words: "validation", "initialization"
- Module headers: "Package for...", "Module for..."

### Claims That Get KEPT

**Theoretical Foundations:**
- "Lyapunov stability theorem" ✅
- "Sliding surface design" ✅
- "PSO convergence analysis" ✅

**Mathematical Methods:**
- "Monte Carlo method" (theory) ✅
- "Bootstrap confidence intervals" (statistical theory) ✅
- "RK45 algorithm" (numerical method) ✅

**Physical Models:**
- "Double inverted pendulum dynamics" ✅
- "Lagrangian mechanics formulation" ✅

---

## Example: Valid vs Invalid Claims

### ❌ INVALID (Skipped)

```
CLAIM: "Enterprise Controller Factory - Production-Ready Controller Instantiation"
REASON: Software design pattern (Factory pattern from GoF)
SKIP: No citation needed
```

```
CLAIM: "None (attributed to: None)"
REASON: Malformed parsing error
SKIP: Cannot research
```

```
CLAIM: "Statistical analysis package for control system benchmarking"
REASON: Module organization description
SKIP: No theoretical content
```

### ✅ VALID (Kept)

```
CLAIM: "Lyapunov stability analysis for sliding mode control"
REASON: Theoretical concept requiring citation
RESEARCH: Cite Lyapunov theorem, SMC stability proofs
```

```
CLAIM: "Particle Swarm Optimization convergence criteria"
REASON: Algorithm theory
RESEARCH: Cite PSO convergence analysis papers
```

```
CLAIM: "Monte Carlo method for statistical validation"
REASON: Statistical method (theory, not implementation)
RESEARCH: Cite Monte Carlo method foundations
```

---

## Batch Status Quick Check

### Check Individual Batch

```bash
cd D:\Projects\main\artifacts\research_batches
ls [batch_id]/SKIP_NOTICE.md
```

**Output:**
- File exists → Skip this batch
- File not found → Batch is valid

### Check All Batches

```bash
cd D:\Projects\main
python -c "
from pathlib import Path
batches = Path('artifacts/research_batches').glob('[0-9]*')
for batch in sorted(batches):
    skip_file = batch / 'SKIP_NOTICE.md'
    status = 'SKIP' if skip_file.exists() else 'VALID'
    print(f'{status:5} - {batch.name}')
"
```

**Output Example:**
```
VALID - 01_CRITICAL_sliding_mode_classical
VALID - 02_CRITICAL_pso_optimization
...
SKIP  - 12_HIGH_benchmarking_performance
VALID - 13_HIGH_pso_optimization
```

---

## Filtering Statistics

### Batch 12 Results

| Metric | Value |
|--------|-------|
| **Total Claims** | 17 |
| **Filtered** | 17 (100%) |
| **Valid** | 0 |
| **Time Saved** | 3.4 hours |

### Pattern Distribution (Batch 12)

| Pattern Type | Count | % |
|--------------|-------|---|
| **Malformed** | 13 | 76% |
| **Software Patterns** | 3 | 18% |
| **Implementation** | 1 | 6% |

---

## Troubleshooting

### Q: "Batch folder is empty after regeneration"

**A:** Batch had zero valid claims after filtering. Check for `SKIP_NOTICE.md`.

### Q: "ChatGPT still providing citations for software patterns"

**A:** Make sure you're using the enhanced prompt with "IMPORTANT - Citation Scope" section.
If using old prompt, regenerate batch with updated generator.

### Q: "Valid claim got filtered"

**A:** Check filter logic in `generate_batch_folders.py::_should_skip_claim()`.
If false positive, update skip_patterns list and regenerate.

### Q: "How do I apply filter to existing CSV?"

**A:** Run:
```python
from generate_batch_folders import BatchFolderGenerator
gen = BatchFolderGenerator(Path('.'))
claim = {'Research_Description': '...', 'Full_Claim_Text': '...'}
should_skip = gen._should_skip_claim(claim)
```

---

## Future Improvements

### Planned Enhancements

1. **Automated Skip Detection**
   - Run filter on all batches
   - Auto-generate skip notices
   - Update batch index

2. **Filter Refinement**
   - ML-based classification
   - Confidence scoring
   - Edge case handling

3. **Upstream Fix**
   - Improve `code_extractor.py`
   - Filter at extraction time
   - Validate docstring quality

---

## Quick Commands

### Test Filter on Single Claim

```bash
cd D:\Projects\main
python -c "
import sys
sys.path.insert(0, 'artifacts/research_batches/_AUTOMATION')
from generate_batch_folders import BatchFolderGenerator
from pathlib import Path

gen = BatchFolderGenerator(Path('.'))
claim = {
    'Research_Description': 'YOUR_CLAIM_TEXT',
    'Full_Claim_Text': 'FULL_CONTEXT'
}
print('SKIP' if gen._should_skip_claim(claim) else 'KEEP')
"
```

### Regenerate Single Batch

```bash
cd D:\Projects\main
python -c "
import sys
sys.path.insert(0, 'artifacts/research_batches/_AUTOMATION')
from generate_batch_folders import BatchFolderGenerator
from pathlib import Path

gen = BatchFolderGenerator(Path('.'))
batch_info = {
    'batch_id': '12_HIGH_benchmarking_performance',
    'priority': 'HIGH',
    'topic': 'benchmarking_performance',
    'claim_count': 17,
    'estimated_time_hours': 3.4,
    'claim_ids': ['CODE-IMPL-048', ...]  # Your claim IDs
}
gen.create_batch_folder(batch_info)
"
```

---

## Resources

- **Optimization Report:** `PROMPT_OPTIMIZATION_REPORT.md`
- **Batch 12 Analysis:** `12_HIGH_benchmarking_performance/SKIP_NOTICE.md`
- **Generator Code:** `_AUTOMATION/generate_batch_folders.py`
- **Main Workflow:** `RESEARCH_WORKFLOW_GUIDE.md`

---

**Version:** 2.0 (Optimized)
**Maintainer:** Claude Code
**Last Updated:** 2025-10-03
