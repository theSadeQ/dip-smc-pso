# Citation System - Phase 4: Validation & Quality Assurance

**Document Version:** 1.0.0
**Created:** 2025-01-15
**Status:** Planning Phase
**Estimated Duration:** Week 8 (10-15 hours)

---

## Phase Overview

**Objective:** Validate citation quality, consistency, and accessibility.

**Input:**
- 500+ cited claims in documentation and code
- `docs/references/enhanced_bibliography.bib` (150-200 entries)

**Output:**
- Zero broken citations
- 100% format consistency
- Validated DOI accessibility
- Citation quality report

---

## Validation Categories

### 1. Link Validation

**Objective:** Verify all DOIs are accessible

**Process:**
```python
# example-metadata:
# runnable: false

class DOIValidator:
    \"\"\"Validate DOI accessibility.\"\"\"

    async def validate_doi(self, doi: str) -> bool:
        \"\"\"Check if DOI resolves successfully.\"\"\"
        url = f"https://doi.org/{doi}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    return response.status == 200
            except Exception as e:
                logging.error(f"DOI {doi} failed: {e}")
                return False

    async def validate_all_dois(
        self,
        bibliography: Path
    ) -> Dict[str, bool]:
        \"\"\"Validate all DOIs in bibliography.\"\"\"
        bib = parse_bibtex(bibliography)

        results = await asyncio.gather(*[
            self.validate_doi(entry.get('doi'))
            for entry in bib.values()
            if 'doi' in entry
        ])

        return dict(zip(bib.keys(), results))
```

**Acceptance Criteria:**
- ≥95% DOIs accessible (HTTP 200)
- Failed DOIs have fallback URLs
- All inaccessible DOIs documented

---

### 2. Duplicate Detection

**Objective:** Identify and merge duplicate citations

**Detection Criteria:**
1. **Exact DOI match** - Same DOI, different citation key
2. **Fuzzy title match** - Similar titles (Levenshtein distance < 5)
3. **Author-year match** - Same first author + year

**Automated Deduplication:**
```python
# example-metadata:
# runnable: false

class DuplicateDetector:
    \"\"\"Detect duplicate BibTeX entries.\"\"\"

    def find_duplicates(
        self,
        bibliography: Path
    ) -> List[DuplicateGroup]:
        \"\"\"Find duplicate entries.\"\"\"
        bib = parse_bibtex(bibliography)

        # Group by DOI
        doi_groups = self.group_by_doi(bib)

        # Group by fuzzy title match
        title_groups = self.group_by_title(bib)

        # Group by author-year
        author_groups = self.group_by_author_year(bib)

        # Merge groups
        duplicates = self.merge_groups(
            doi_groups,
            title_groups,
            author_groups
        )

        return duplicates

    def resolve_duplicates(
        self,
        duplicates: List[DuplicateGroup]
    ) -> Dict[str, str]:
        \"\"\"Select canonical citation for each duplicate group.\"\"\"
        resolution = {}

        for group in duplicates:
            # Select most complete entry as canonical
            canonical = max(group, key=lambda e: self.completeness_score(e))

            for entry in group:
                if entry != canonical:
                    resolution[entry.key] = canonical.key

        return resolution
```

---

### 3. Citation Style Consistency

**Objective:** Enforce IEEE citation style

**IEEE Style Requirements:**
1. **Author format:** "LastName, F. M."
2. **Title:** Sentence case with quotes
3. **Journal:** Italicized abbreviation
4. **Year:** Parentheses
5. **DOI:** Full URL format

**Style Validation:**
```python
# example-metadata:
# runnable: false

class StyleValidator:
    \"\"\"Validate IEEE citation style.\"\"\"

    def validate_entry(self, entry: BibTeXEntry) -> List[StyleError]:
        \"\"\"Check entry for IEEE style compliance.\"\"\"
        errors = []

        # Author format
        if not self.is_ieee_author_format(entry.get('author')):
            errors.append(StyleError(
                field='author',
                expected='LastName, F. M.',
                actual=entry.get('author')
            ))

        # Title capitalization
        if not self.is_sentence_case(entry.get('title')):
            errors.append(StyleError(
                field='title',
                expected='Sentence case',
                actual=entry.get('title')
            ))

        # Journal abbreviation
        if 'journal' in entry:
            if not self.is_ieee_journal_abbrev(entry['journal']):
                errors.append(StyleError(
                    field='journal',
                    expected='IEEE abbreviated form',
                    actual=entry['journal']
                ))

        return errors

    def auto_fix_style(
        self,
        entry: BibTeXEntry
    ) -> BibTeXEntry:
        \"\"\"Automatically fix common style issues.\"\"\"
        # Convert author names to IEEE format
        entry['author'] = self.convert_author_format(entry['author'])

        # Convert title to sentence case
        entry['title'] = self.convert_to_sentence_case(entry['title'])

        # Abbreviate journal name
        if 'journal' in entry:
            entry['journal'] = self.abbreviate_journal(entry['journal'])

        return entry
```

---

### 4. Claim Coverage Validation

**Objective:** Ensure ≥85% of claims are cited

**Coverage Analysis:**
```python
# example-metadata:
# runnable: false

class CoverageAnalyzer:
    \"\"\"Analyze citation coverage of claims.\"\"\"

    def analyze_coverage(
        self,
        claims_inventory: Path,
        citation_mapping: Path
    ) -> CoverageReport:
        \"\"\"Calculate claim citation coverage.\"\"\"
        claims = load_json(claims_inventory)
        mapping = load_json(citation_mapping)

        total_claims = len(claims)
        cited_claims = len([
            c for c in claims
            if c['id'] in mapping and len(mapping[c['id']]) > 0
        ])

        coverage = cited_claims / total_claims * 100

        # Breakdown by claim priority
        critical_claims = [c for c in claims if c['priority'] == 'CRITICAL']
        critical_cited = len([
            c for c in critical_claims
            if c['id'] in mapping and len(mapping[c['id']]) > 0
        ])

        return CoverageReport(
            total_claims=total_claims,
            cited_claims=cited_claims,
            coverage_percentage=coverage,
            critical_coverage=critical_cited / len(critical_claims) * 100
        )
```

---

## Validation Tools

### 1. Comprehensive Validation Script

**File:** `scripts/citations/validate_bibliography.py`

**Features:**
- DOI accessibility checks
- Duplicate detection
- Style consistency validation
- Coverage analysis
- Automated fixing where possible

**Usage:**
```bash
# Run all validations
python scripts/citations/validate_bibliography.py --all

# DOI validation only
python scripts/citations/validate_bibliography.py --check-dois

# Style validation with auto-fix
python scripts/citations/validate_bibliography.py --check-style --auto-fix

# Duplicate detection
python scripts/citations/validate_bibliography.py --find-duplicates
```

---

### 2. Citation Quality Report Generator

**File:** `scripts/citations/generate_citation_report.py`

**Output:** `artifacts/citation_quality_report.html`

**Report Sections:**
1. **Executive Summary**
   - Total citations: 187
   - DOI accessibility: 96.8%
   - Duplicate count: 3
   - Style compliance: 98.5%
   - Claim coverage: 87.2%

2. **Quality Metrics**
   - Citation distribution by type (journal, conference, preprint)
   - Average citation count per reference
   - Venue quality distribution (top-tier, mid-tier, other)

3. **Validation Results**
   - DOI validation table (accessible/broken)
   - Duplicate groups identified
   - Style errors detected
   - Uncited claims list

4. **Recommendations**
   - High-priority fixes
   - Citation gaps to fill
   - Quality improvement suggestions

---

## Deliverables

### 1. Validation Report

**File:** `artifacts/citation_validation_report.json`

```json
{
  "doi_validation": {
    "total_dois": 187,
    "accessible": 181,
    "broken": 6,
    "success_rate": 96.8
  },
  "duplicate_detection": {
    "duplicate_groups": 2,
    "total_duplicates": 3,
    "resolution": {
      "Utkin1999a": "Utkin1999",
      "Edwards1998b": "Edwards1998"
    }
  },
  "style_consistency": {
    "total_entries": 187,
    "compliant": 184,
    "errors": 3,
    "compliance_rate": 98.4
  },
  "claim_coverage": {
    "total_claims": 512,
    "cited_claims": 446,
    "coverage_percentage": 87.1,
    "critical_coverage": 95.2
  }
}
```

### 2. Fixed Bibliography

**File:** `docs/references/enhanced_bibliography_validated.bib`

- All duplicates merged
- Style errors corrected
- Broken DOIs replaced with fallback URLs
- Sorted by citation key

### 3. Broken Links Fallback

**File:** `artifacts/broken_dois_fallback.json`

```json
{
  "Moreno2008": {
    "doi": "10.1109/TAC.2008.INVALID",
    "status": "404",
    "fallback_url": "https://ieeexplore.ieee.org/document/XXXXX",
    "alternative_sources": [
      "ResearchGate: https://researchgate.net/...",
      "Author page: https://..."
    ]
  }
}
```

---

## Acceptance Criteria

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **DOI Accessibility** | ≥95% | TBD | Pending |
| **Duplicate Rate** | <2% | TBD | Pending |
| **Style Compliance** | 100% | TBD | Pending |
| **Claim Coverage** | ≥85% | TBD | Pending |
| **Critical Claim Coverage** | ≥95% | TBD | Pending |

---

## Quality Assurance Tests

### Automated Test Suite

**File:** `tests/test_documentation/test_citations.py`

```python
# example-metadata:
# runnable: false

def test_doi_accessibility(bibliography):
    \"\"\"Verify all DOIs are accessible.\"\"\"
    validator = DOIValidator()
    results = validator.validate_all_dois(bibliography)

    broken_dois = [doi for doi, accessible in results.items() if not accessible]

    assert len(broken_dois) / len(results) < 0.05, \
        f"Too many broken DOIs: {broken_dois}"


def test_no_duplicates(bibliography):
    \"\"\"Verify no duplicate entries exist.\"\"\"
    detector = DuplicateDetector()
    duplicates = detector.find_duplicates(bibliography)

    assert len(duplicates) == 0, \
        f"Found duplicate citation groups: {duplicates}"


def test_style_consistency(bibliography):
    \"\"\"Verify IEEE style compliance.\"\"\"
    validator = StyleValidator()

    bib = parse_bibtex(bibliography)
    errors = []

    for key, entry in bib.items():
        errors.extend(validator.validate_entry(entry))

    assert len(errors) == 0, \
        f"Found style errors: {errors}"


def test_claim_coverage(claims_inventory, citation_mapping):
    \"\"\"Verify adequate claim citation coverage.\"\"\"
    analyzer = CoverageAnalyzer()
    report = analyzer.analyze_coverage(claims_inventory, citation_mapping)

    assert report.coverage_percentage >= 85.0, \
        f"Coverage {report.coverage_percentage}% < 85%"

    assert report.critical_coverage >= 95.0, \
        f"Critical coverage {report.critical_coverage}% < 95%"
```

---

## Execution Plan

### Week 8: Validation & Quality (10-15 hours)

**Day 1-2: Automated Validation (5h)**
- Implement validation tools
- Run DOI accessibility checks
- Detect and resolve duplicates
- Fix style inconsistencies

**Day 3-4: Coverage Analysis (3h)**
- Analyze claim citation coverage
- Identify uncited critical claims
- Generate coverage report

**Day 5: Manual Review (4h)**
- Review top 50 critical citations
- Verify technical accuracy
- Check citation relevance
- Fix identified issues

**Day 6: Final Quality Checks (3h)**
- Run comprehensive test suite
- Generate final quality report
- Create documentation
- Prepare for Phase 5

---

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Many broken DOIs** | MEDIUM | Provide fallback URLs, author pages |
| **High duplicate rate** | LOW | Automated resolution with manual review |
| **Style inconsistencies** | LOW | Automated fixing for most cases |
| **Low coverage** | HIGH | Identify gaps, run additional research (mini Phase 2) |

---

## Dependencies

- **Phase 3 Complete:** Citations inserted in all documentation and code
- **Bibliography:** `enhanced_bibliography.bib` with 150-200 entries
- **Python Libraries:** `aiohttp`, `bibtexparser`, `fuzzywuzzy`

---

## Next Phase

**Phase 5:** [Final Review & Publication](./06_phase5_final_review.md)

---

**Related Documents:**
- [Master Roadmap](./00_master_roadmap.md)
- [Phase 3: Citation Integration](./04_phase3_citation_integration.md)
