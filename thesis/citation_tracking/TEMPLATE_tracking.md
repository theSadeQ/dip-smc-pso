# [Author][Year] Citation Tracking Template

**PDF File**: `filename.pdf`
**BibTeX Key**: `AuthorYear`
**Full Title**: Full title of the paper/book
**Authors**: Author names
**Journal/Publisher**: Where published
**Year**: Publication year
**Pages**: Total page count (PDF vs document numbering)

**Date Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

---

## Document Structure Overview

| Section | PDF Pages | Doc Pages | Content Summary |
|---------|-----------|-----------|-----------------|
| Abstract | 1 | 576 | Brief summary |
| Section 1: Introduction | 2-3 | 577-578 | Background, motivation |
| Section 2: Problem Statement | 4 | 579 | System definition |
| ... | ... | ... | ... |

---

## Tracked Content

### Section 1: Introduction (pp. XXX-YYY)

**Used in Thesis**: Section 2.2 (Background on Topic X)

**Content Summary**:
Brief description of what this section contains and why it's relevant.

**LaTeX Citations**:
```latex
% General background
The concept was introduced in \cite[pp.~XXX--YYY]{AuthorYear}.

% Specific point
As noted by \cite[p.~XXX]{AuthorYear}, the system exhibits...
```

**Key Points**:
- First key point from this section
- Second key point
- Third key point

**Equations**: None / List equation numbers

**Figures/Tables**: None / List figure/table numbers

---

### Theorem 1: Theorem Name (p. XXX)

**Used in Thesis**: Section 3.1 (Proof of Stability)

**Theorem Statement**:
```
[Copy theorem statement exactly as it appears in PDF]
```

**LaTeX Citation**:
```latex
Finite-time convergence is guaranteed by \cite[Theorem~1, p.~XXX]{AuthorYear}.
```

**Related Content**:
- Proof sketch: pp. XXX-YYY
- Corollaries: List if any
- Applications: Where theorem is used

---

### Equation (N): Equation Name (p. XXX)

**Used in Thesis**: Section 3.4, Equation (3.12)

**Equation**:
```latex
\begin{equation}
  % Copy equation here
\end{equation}
```

**LaTeX Citation**:
```latex
The controller \cite[Eq.~(N), p.~XXX]{AuthorYear} is defined as...
```

**Parameters**:
- α: Parameter description
- β: Parameter description
- ...

**Context**: Brief explanation of where/how this equation is used

---

### Figure N: Figure Title (p. XXX)

**Used in Thesis**: Section 5.2 (Results Validation)

**Figure Description**:
Description of what the figure shows (e.g., phase portrait, time response).

**LaTeX Citation**:
```latex
Our results (Fig. 5.2) match \cite[Fig.~N, p.~XXX]{AuthorYear}.
```

**Key Observations**:
- What the figure demonstrates
- Important features to note

---

### Algorithm N: Algorithm Name (pp. XXX-YYY)

**Used in Thesis**: Section 4.3 (Implementation)

**Algorithm Steps**:
1. Step 1
2. Step 2
3. ...

**LaTeX Citation**:
```latex
% Code comment
% Based on \cite[Algorithm~N, pp.~XXX--YYY]{AuthorYear}
```

**Parameters**:
- Input parameters
- Output parameters
- Tuning parameters

---

## Quick Reference Table

| Content Type | Location | Thesis Section | Citation |
|--------------|----------|----------------|----------|
| Introduction | pp. XXX-YYY | 2.2 | `\cite[pp.~XXX--YYY]{AuthorYear}` |
| Theorem 1 | p. XXX | 3.1 | `\cite[Theorem~1, p.~XXX]{AuthorYear}` |
| Equation (N) | p. XXX | 3.4 | `\cite[Eq.~(N), p.~XXX]{AuthorYear}` |
| Figure N | p. XXX | 5.2 | `\cite[Fig.~N, p.~XXX]{AuthorYear}` |
| Algorithm N | pp. XXX-YYY | 4.3 | `\cite[Algorithm~N]{AuthorYear}` |

---

## Citation Statistics

**Total Citations in Thesis**: 0
**Sections Referenced**: 0
**Equations Cited**: 0
**Theorems Cited**: 0
**Figures Cited**: 0

---

## Notes

### Important Passages

**Page XXX** (Section X.Y):
> "Quote important passage here"

**Relevance**: Why this passage matters for thesis.

**Citation**:
```latex
As stated by \cite[p.~XXX]{AuthorYear}, "quoted text".
```

---

### Cross-References to Other Papers

**Related to [OtherAuthor][OtherYear]**:
- This paper extends/contradicts/complements the work in [OtherPaper]
- Section X in this paper corresponds to Section Y in [OtherPaper]

---

### Implementation Details

**Parameters Used in Code**:
- Parameter: Value (from p. XXX)
- Parameter: Value (from Table N, p. YYY)

**Source Code References**:
```python
# src/controllers/example_controller.py:42
# Parameters from \cite[Table~N, p.~XXX]{AuthorYear}
alpha = 0.5  # Eq. (N), p. XXX
beta = 1.0   # Eq. (M), p. YYY
```

---

### Open Questions

1. **Question about unclear concept**
   - Source: Section X, p. YYY
   - Status: [RESOLVED] / [PENDING]
   - Resolution: How it was resolved

---

## BibTeX Entry

```bibtex
@article{AuthorYear,
  author  = {Author Name},
  title   = {Full Title},
  journal = {Journal Name},
  year    = {YYYY},
  volume  = {XX},
  number  = {Y},
  pages   = {XXX--YYY},
  doi     = {10.xxxx/xxxxx}
}
```

**Status**: [ ] Added to references.bib  [ ] Verified complete

---

## Checklist

### Initial Setup
- [ ] PDF file location confirmed
- [ ] BibTeX key assigned
- [ ] Document structure mapped
- [ ] Page numbering clarified (PDF vs document)

### Content Extraction
- [ ] Key sections identified
- [ ] Theorems/lemmas extracted
- [ ] Important equations noted
- [ ] Relevant figures listed
- [ ] Algorithms documented

### Thesis Integration
- [ ] Citations added to thesis
- [ ] Tracking updated with thesis section numbers
- [ ] Cross-references verified
- [ ] BibTeX entry added to references.bib

### Quality Assurance
- [ ] Page numbers verified
- [ ] Citations formatted consistently
- [ ] No duplicate citations
- [ ] All references in thesis are tracked

---

## Usage Instructions

### Creating a New Tracking File

1. **Copy this template**: `cp TEMPLATE_tracking.md AuthorYear_tracking.md`
2. **Fill in header**: PDF filename, BibTeX key, title, authors
3. **Request AI extraction**: "Read [PDF] and populate tracking file"
4. **Verify accuracy**: Check page numbers, equations, theorems
5. **Link to thesis**: Update "Used in Thesis" fields as you write

### Requesting AI Population

**Example requests**:
```
"Read Levant2007 and create tracking file using template"
"Extract all theorems from Khalil2002 into tracking file"
"Find PSO algorithm in Kennedy1995 and update tracking file"
"List all equations from Section 3 of Shtessel2014"
```

### Updating Tracking File

**When writing thesis**:
1. Use citation from tracking file
2. Update "Used in Thesis" field
3. Increment citation statistics
4. Add notes if needed

**Example**:
```markdown
### Theorem 1: Finite-Time Stability (p. 578)
**Used in Thesis**: Section 3.1 (Proof of Stability) ← ADD THIS
```

---

## See Also

- [Master Index](INDEX.md) - All tracked PDFs
- [AI Citation Workflow](../../docs/thesis/AI_CITATION_WORKFLOW.md) - How to use AI for citations
- `thesis/references.bib` - BibTeX database

---

**Status**: [TEMPLATE] Ready to copy and populate

**Last Updated**: 2025-12-06
