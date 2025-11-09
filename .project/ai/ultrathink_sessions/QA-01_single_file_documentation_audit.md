# QA-01: Single File Documentation Audit

**Type**: Quick Audit
**Duration**: 2 hours
**Scope**: Single documentation file

---

## Session Prompt

```
SINGLE FILE DOCUMENTATION AUDIT
WHAT: Analyze [filename] for completeness, accuracy, readability, accessibility
WHY:  Verify quality of critical documentation file before user-facing release
HOW:  Manual review + automated metrics (word count, headings, links)
WIN:  Complete quality report with specific improvement actions
TIME: 2 hours

TARGET FILE: [INSERT FILENAME HERE]

INPUTS:
- Target file: [path/to/file.md]
- Expected audience: [beginner/intermediate/advanced/researcher]
- Expected use case: [learning/reference/tutorial/research]

ANALYSIS TASKS:
1. COMPLETENESS (30 min)
   - Does it cover all topics in its scope?
   - Are there gaps in explanation?
   - Are all sections finished (no TODOs)?
   - Document missing topics

2. ACCURACY (30 min)
   - Verify code examples execute correctly
   - Check technical claims against source code
   - Validate equations/formulas
   - Document 5+ specific facts to verify

3. READABILITY (30 min)
   - Calculate Flesch Reading Ease
   - Count passive voice sentences
   - Check sentence length (avg, max)
   - Identify jargon without definitions

4. ACCESSIBILITY (30 min)
   - Check heading hierarchy (H1 → H2 → H3)
   - Verify alt text on images
   - Test link text (avoid "click here")
   - Check code blocks have language tags

VALIDATION REQUIREMENTS:
1. Execute all code examples (if any)
2. Manually verify 5+ technical claims
3. Read full file for coherence

DELIVERABLES:
1. Quality scorecard (4 metrics: completeness, accuracy, readability, accessibility)
2. List of specific issues (with line numbers)
3. Prioritized fix recommendations (with effort estimates)
4. Raw metrics file (JSON)

SUCCESS CRITERIA:
- [ ] All 4 analysis tasks completed
- [ ] 5+ technical claims verified manually
- [ ] All code examples tested
- [ ] Specific line numbers for each issue
- [ ] Effort estimates for each recommendation
- [ ] Can answer: "Is this file ready for users?"
```

---

## Example Usage

```
SINGLE FILE DOCUMENTATION AUDIT
WHAT: Analyze docs/guides/getting-started.md for completeness, accuracy, readability, accessibility
WHY:  Verify quality of critical getting-started guide before user-facing release
HOW:  Manual review + automated metrics (word count, headings, links)
WIN:  Complete quality report with specific improvement actions
TIME: 2 hours

TARGET FILE: docs/guides/getting-started.md

INPUTS:
- Target file: docs/guides/getting-started.md
- Expected audience: beginner
- Expected use case: tutorial

[Continue with analysis tasks...]
```

---

## Common Targets

- Getting started guides
- Tutorial files
- Theory documentation
- API reference pages
- Configuration guides
- README files
