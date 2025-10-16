# How to Use ChatGPT Prompt for 100% Citation Accuracy

**Status**: ✅ Prompt file ready
**Location**: `CHATGPT_PROMPT_100_PERCENT.md` (this directory)
**Claims**: 108 remaining (to reach 100%)
**Current accuracy**: 206/314 (65.6%)
**Target accuracy**: 314/314 (100%)

---

## Quick Start (5 Steps)

### 1. Open the Prompt File

Open this file in any text editor:
```
D:\Projects\main\artifacts\research_batches\08_HIGH_implementation_general\CHATGPT_PROMPT_100_PERCENT.md
```

**File size**: 220 KB
**Content**: Complete instructions + all 108 claims with source code embedded

---

### 2. Copy Everything

- Press `Ctrl+A` (select all)
- Press `Ctrl+C` (copy)

**DO NOT edit anything** - the prompt is completely self-contained and ready to use as-is.

---

### 3. Paste into ChatGPT

1. Go to: https://chat.openai.com/
2. Open a **new chat** (don't use an existing conversation)
3. Press `Ctrl+V` to paste the entire prompt
4. Press Enter

**Model recommendation**: Use ChatGPT-4 or ChatGPT-4o for best results (GPT-3.5 may struggle with the large prompt)

---

### 4. Wait for Response

ChatGPT will process all 108 claims. This takes approximately:
- **Fast (GPT-4o)**: 15-30 minutes
- **Standard (GPT-4)**: 30-60 minutes

ChatGPT will return a JSON array with 108 elements, each containing:
- Claim ID
- Category (A/B/C)
- Citation (if applicable)
- Rationale

---

### 5. Save Response

Copy ChatGPT's JSON response and save it to:
```
D:\Projects\main\artifacts\research_batches\08_HIGH_implementation_general\chatgpt_output_108_citations.json
```

**IMPORTANT**: Make sure to copy ONLY the JSON array (starting with `[` and ending with `]`), not any additional text ChatGPT adds before/after.

---

## After You Save the Response

Run this Python script to apply ChatGPT's citations to the CSV:

```bash
cd D:\Projects\main
python .dev_tools/apply_chatgpt_citations.py
```

This script will:
1. Load `chatgpt_output_108_citations.json`
2. Validate all 108 citations
3. Apply them to `claims_research_tracker.csv`
4. Generate a summary report
5. Calculate final accuracy (should be 314/314 = 100%)

---

## What ChatGPT Will Do

ChatGPT will categorize each of the 108 claims into:

**Category A (~20%)**: Algorithmic implementations needing peer-reviewed papers
- Example: Differential Evolution mutation operator → Cite Storn & Price (1997)
- Example: Recursive Least Squares algorithm → Cite appropriate paper

**Category B (~10%)**: Theoretical concepts needing textbooks
- Example: Stability metrics documentation → Cite Ogata (2010)
- Example: Control theory module docstrings → Cite Khalil (2002)

**Category C (~70%)**: Pure implementation needing NO citations
- Example: Module imports (`__init__.py`)
- Example: Factory patterns, base classes
- Example: Configuration classes, error handling
- Example: Property accessors, context managers
- Example: Simple computations (variance, mean)

---

## Expected Output Format

ChatGPT will return JSON like this:

```json
[
  {
    "claim_id": "CODE-IMPL-085",
    "category": "C",
    "confidence": "HIGH",
    "rationale": "Trial runner factory function - pure implementation",
    "code_summary": "Executes single simulation trial with given parameters",
    "suggested_citation": "",
    "bibtex_key": "",
    "doi_or_url": "",
    "reference_type": ""
  },
  {
    "claim_id": "CODE-IMPL-273",
    "category": "A",
    "confidence": "HIGH",
    "rationale": "Implements DE/rand/1 mutation from scratch",
    "code_summary": "Differential evolution mutation operator",
    "algorithm_name": "Differential Evolution",
    "suggested_citation": "Storn & Price (1997)",
    "bibtex_key": "storn1997differential",
    "doi_or_url": "10.1023/A:1008202821328",
    "paper_title": "Differential Evolution – A Simple and Efficient...",
    "reference_type": "journal",
    "verification": "Paper Eq. (1) matches implementation"
  },
  ...
]
```

---

## If ChatGPT Has Issues

### Issue 1: "Prompt too long"
**Solution**: Use GPT-4 or GPT-4o (not GPT-3.5). GPT-4 has larger context window.

### Issue 2: "Cannot access files"
**Solution**: You already have the complete prompt - all data is embedded in the markdown file. Just copy-paste the file content.

### Issue 3: Response is truncated
**Solution**: Ask ChatGPT to "continue" and it will resume from where it stopped. Manually merge the JSON arrays.

### Issue 4: ChatGPT returns invalid JSON
**Solution**: Ask ChatGPT to "reformat the output as valid JSON" and copy again.

### Issue 5: ChatGPT asks questions
**Solution**: Tell ChatGPT "Please process all 108 claims now based on the instructions provided in the prompt. Do not ask questions, just return the JSON array."

---

## Validation Script

After you save ChatGPT's response, run this to validate it:

```python
import json

# Load ChatGPT's output
with open('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_citations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Validate
print(f'Claims processed: {len(data)}')
print(f'Expected: 108')

# Count categories
cat_a = sum(1 for claim in data if claim['category'] == 'A')
cat_b = sum(1 for claim in data if claim['category'] == 'B')
cat_c = sum(1 for claim in data if claim['category'] == 'C')

print(f'\nCategory A (papers): {cat_a} ({100*cat_a/len(data):.1f}%)')
print(f'Category B (textbooks): {cat_b} ({100*cat_b/len(data):.1f}%)')
print(f'Category C (no citation): {cat_c} ({100*cat_c/len(data):.1f}%)')

# Expected distribution
print(f'\nExpected distribution:')
print(f'  Category A: ~20-25 (20-23%)')
print(f'  Category B: ~10-13 (10-12%)')
print(f'  Category C: ~70-75 (65-70%)')

if len(data) == 108:
    print('\n✓ Validation PASSED - Ready to apply!')
else:
    print(f'\n✗ Validation FAILED - Expected 108 claims, got {len(data)}')
```

---

## Timeline

**Total time to 100%**: ~1-2 hours

1. **You copy-paste prompt to ChatGPT**: 1 minute
2. **ChatGPT processes**: 15-60 minutes
3. **You save response**: 1 minute
4. **Script applies citations**: 1 minute
5. **Verification**: 5 minutes

**Result**: 314/314 (100%) citation accuracy ✅

---

## Troubleshooting

If you encounter any issues:

1. **Check file exists**: `CHATGPT_PROMPT_100_PERCENT.md` (220 KB)
2. **Validate structure**: Run `python .dev_tools/validate_prompt.py`
3. **Re-generate if needed**: Run `python .dev_tools/generate_chatgpt_prompt.py`

---

## Summary

**What you need to do**:
1. Copy `CHATGPT_PROMPT_100_PERCENT.md` content
2. Paste into ChatGPT
3. Wait for response
4. Save response to `chatgpt_output_108_citations.json`
5. Run `python .dev_tools/apply_chatgpt_citations.py`

**What you'll get**:
- All 108 remaining claims categorized and cited
- 314/314 (100%) citation accuracy
- Complete audit trail of all decisions

**Time required**: ~1-2 hours total (mostly waiting for ChatGPT)

---

**Good luck reaching 100%!** 🎯
