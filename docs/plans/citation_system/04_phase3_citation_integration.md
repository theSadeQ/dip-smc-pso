# Citation System - Phase 3: Citation Integration

**Document Version:** 1.0.0
**Created:** 2025-01-15
**Status:** Planning Phase
**Estimated Duration:** Week 5-7 (15-25 hours)

---

## Phase Overview

**Objective:** Insert 150-200 verified citations into documentation and code docstrings.

**Input:**
- `artifacts/citation_mapping.json` (from Phase 2)
- `docs/references/enhanced_bibliography.bib` (150-200 entries)

**Output:**
- 500+ claims cited in documentation
- All docstrings updated with proper citations
- Citation style consistency enforced

---

## Citation Integration Strategy

### 1. Documentation Files

**Target:** Markdown documentation files (`.md`)

**Citation Format:**
```markdown
The super-twisting algorithm eliminates chattering [[Levant2001]](#ref-Levant2001)
through continuous control approximation [[Moreno2012]](#ref-Moreno2012).

## References

<a name="ref-Levant2001"></a>
[Levant2001] Levant, A. (2001). "Super-twisting algorithm for second-order
sliding mode." IEEE Transactions on Automatic Control, 46(1), 133-135.
```

### 2. Python Docstrings

**Target:** Class and function docstrings

**Citation Format:**
```python
# example-metadata:
# runnable: false

def super_twisting_control(state, gains):
    \"\"\"Compute super-twisting sliding mode control.

    Implements the continuous super-twisting algorithm which eliminates
    chattering through second-order sliding mode [1]_.

    Parameters
    ----------
    state : np.ndarray
        System state vector
    gains : Dict[str, float]
        Controller gains (alpha, beta)

    Returns
    -------
    float
        Control signal

    References
    ----------
    .. [1] Levant, A. (2001). "Super-twisting algorithm for second-order
       sliding mode." IEEE Transactions on Automatic Control, 46(1), 133-135.
       https://doi.org/10.1109/TAC.2001.964620

    .. [2] Moreno, J. A., & Osorio, M. (2012). "Strict Lyapunov functions
       for the super-twisting algorithm." IEEE TAC, 57(4), 1035-1040.
    \"\"\"
```

---

## Tool Development

### 1. Citation Insertion Tool (`scripts/citations/insert_citations.py`)

**Estimated Effort:** 350 lines, 12 hours

```python
# example-metadata:
# runnable: false

class CitationInserter:
    \"\"\"Insert citations into documentation and code.\"\"\"

    def __init__(
        self,
        citation_mapping: Path,
        bibliography: Path,
        dry_run: bool = False
    ):
        self.mapping = load_json(citation_mapping)
        self.bib = parse_bibtex(bibliography)
        self.dry_run = dry_run

    def insert_into_markdown(
        self,
        file_path: Path,
        claim_ids: List[str]
    ) -> int:
        \"\"\"Insert citations into markdown file.\"\"\"
        content = file_path.read_text()

        for claim_id in claim_ids:
            citations = self.mapping[claim_id]

            # Find claim text in content
            claim_text = self.get_claim_text(claim_id)

            # Insert inline citations
            cited_text = self.add_inline_citations(
                claim_text,
                citations
            )

            content = content.replace(claim_text, cited_text)

        # Add references section
        content = self.add_references_section(content, citations)

        if not self.dry_run:
            file_path.write_text(content)

        return len(citations)

    def insert_into_docstring(
        self,
        file_path: Path
    ) -> int:
        \"\"\"Insert citations into Python docstrings.\"\"\"
        # AST-based docstring modification
        tree = ast.parse(file_path.read_text())

        citations_added = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)

                if docstring and self.has_claim(docstring):
                    new_docstring = self.add_citations_to_docstring(
                        docstring,
                        node.name
                    )

                    # Update AST
                    self.update_docstring(node, new_docstring)
                    citations_added += 1

        if not self.dry_run:
            # Write modified AST back to file
            file_path.write_text(ast.unparse(tree))

        return citations_added
```

**Features:**
- AST-based Python file modification (preserves formatting)
- Markdown citation insertion
- Dry-run mode for validation
- Batch processing support
- Backup creation before modification

---

### 2. Citation Validation Tool (`scripts/citations/validate_insertions.py`)

**Estimated Effort:** 200 lines, 8 hours

```python
# example-metadata:
# runnable: false

class CitationValidator:
    \"\"\"Validate inserted citations.\"\"\"

    def validate_markdown_citations(
        self,
        file_path: Path
    ) -> List[ValidationError]:
        \"\"\"Check markdown citations for correctness.\"\"\"
        errors = []

        content = file_path.read_text()

        # Extract inline citations [[CitationKey]]
        inline_citations = re.findall(r'\[\[([^\]]+)\]\]', content)

        # Extract reference section citations
        ref_citations = self.extract_references(content)

        # Validate all inline citations have references
        for citation in inline_citations:
            if citation not in ref_citations:
                errors.append(ValidationError(
                    file=file_path,
                    citation=citation,
                    error="Missing reference for inline citation"
                ))

        return errors

    def validate_bibtex_references(
        self,
        file_path: Path,
        bibliography: Path
    ) -> List[ValidationError]:
        \"\"\"Check that all citations exist in bibliography.\"\"\"
        errors = []

        # Extract all citation keys from file
        citations = self.extract_all_citations(file_path)

        # Load bibliography
        bib = parse_bibtex(bibliography)

        # Validate existence
        for citation in citations:
            if citation not in bib:
                errors.append(ValidationError(
                    file=file_path,
                    citation=citation,
                    error=f"Citation {citation} not found in bibliography"
                ))

        return errors
```

---

## Execution Plan

### Week 5: Documentation File Citations (10 hours)

**Target Files:**
1. Theory documentation (40 files)
   - `docs/mathematical_foundations/`
   - `docs/theory/`

2. Controller guides (15 files)
   - `docs/controllers/`
   - `docs/reference/controllers/`

3. PSO documentation (10 files)
   - `docs/optimization/`
   - `docs/factory/pso_*.md`

**Process:**
```bash
python scripts/citations/insert_citations.py \
    --target docs/mathematical_foundations \
    --dry-run

python scripts/citations/insert_citations.py \
    --target docs/mathematical_foundations \
    --apply
```

---

### Week 6: Code Docstring Citations (8 hours)

**Target Modules:**
1. Controllers (`src/controllers/`)
2. Plant models (`src/plant/`)
3. PSO optimizer (`src/optimization/`)
4. Analysis (`src/analysis/`)

**Process:**
```bash
python scripts/citations/insert_citations.py \
    --target src/controllers \
    --type docstring \
    --dry-run

python scripts/citations/insert_citations.py \
    --target src/controllers \
    --type docstring \
    --apply
```

---

### Week 7: Validation & Quality Assurance (7 hours)

**Tasks:**
1. Run citation validation
2. Check citation format consistency
3. Verify all citations exist in bibliography
4. Manual review of critical citations
5. Fix validation errors

**Commands:**
```bash
python scripts/citations/validate_insertions.py --all
python scripts/citations/generate_citation_report.py
```

---

## Deliverables

### 1. Cited Documentation Files
- 500+ citations inserted
- References sections added
- Proper citation format

### 2. Updated Code Docstrings
- All claim-bearing docstrings cited
- NumPy docstring format with References section
- Consistent citation style

### 3. Citation Quality Report
**File:** `artifacts/citation_integration_report.json`

```json
{
  "files_processed": 245,
  "citations_inserted": 523,
  "documentation_files": 185,
  "code_files": 60,
  "validation_errors": 0,
  "format_consistency": "100%"
}
```

---

## Acceptance Criteria

| Metric | Target | Validation |
|--------|--------|------------|
| **Citations Inserted** | 500+ | Count citations in files |
| **Coverage** | ≥85% claims cited | Cited claims / total claims |
| **Format Consistency** | 100% | Validation script pass |
| **Broken References** | 0 | All citations in bibliography |
| **Validation Errors** | 0 | No missing/malformed citations |

---

## Quality Assurance

### Automated Tests

```bash
pytest tests/test_documentation/test_citations.py -v
```

**Test Coverage:**
- Citation format validation
- Bibliography consistency
- Inline citation completeness
- Reference section correctness

### Manual Review

**Critical Sections (1 hour each):**
1. SMC theory citations (10 key theorems)
2. PSO algorithm citations (5 key claims)
3. Stability analysis citations (8 proofs)

---

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Incorrect citations** | HIGH | Manual review of top 50 critical claims |
| **Format inconsistency** | MEDIUM | Automated formatting enforcement |
| **Code breakage** | HIGH | AST-based modification + extensive testing |
| **Missing citations** | MEDIUM | Validation script detects all gaps |

---

## Dependencies

- **Phase 2 Complete:** `citation_mapping.json`, `enhanced_bibliography.bib`
- **Python Libraries:** `bibtexparser`, `ast`, `libcst`
- **Validation Tools:** Custom validation scripts

---

## Next Phase

**Phase 4:** [Validation & Quality Assurance](./05_phase4_validation_quality.md)

---

**Related Documents:**
- [Master Roadmap](./00_master_roadmap.md)
- [Phase 2: AI Research](./03_phase2_ai_research.md)
