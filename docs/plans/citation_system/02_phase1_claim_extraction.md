# Phase 1: Claim Extraction Infrastructure - Detailed Implementation Plan

**Document Version:** 1.0.0
**Created:** 2025-01-15
**Duration:** Week 1-2 (15-20 hours)
**Status:** Ready for Implementation

---

## Table of Contents

1. [Phase Overview](#phase-overview)
2. [Tool 1: Formal Mathematical Claim Extractor](#tool-1-formal-mathematical-claim-extractor)
3. [Tool 2: Code Implementation Claim Extractor](#tool-2-code-implementation-claim-extractor)
4. [Tool 3: Claims Database Merger](#tool-3-claims-database-merger)
5. [Validation Strategy](#validation-strategy)
6. [Timeline & Milestones](#timeline--milestones)

---

## Phase Overview

### **Objective**
Build automated claim extraction system to identify and categorize 500+ scientific/technical claims requiring citations.

### **Why Specialized Extractors?**

Different claim types require different extraction strategies:

| Claim Type | Extraction Method | Precision Target | Reasoning |
|------------|-------------------|------------------|-----------|
| **Formal Math** (Theorems) | Regex patterns | 95% | Explicit structure (`**Theorem X**`) |
| **Code Impl** (Docstrings) | AST + Regex | 85% | Structured Python syntax |
| **Performance** (Benchmarks) | Regex + Context | 80% | Quantitative patterns |
| **Domain Knowledge** ("well-known") | NLP (optional) | 70% | Informal language |

**Anti-Pattern (Rejected):**
```python
# example-metadata:
# runnable: false

class MonolithicExtractor:  # ❌ Don't do this
    def extract_all(self, files):
        # 2000+ lines mixing docs + code + math
        # Result: Unmaintainable, low precision
```

**Chosen Pattern:**
```python
# example-metadata:
# runnable: false

class FormalClaimExtractor:    # ✅ Specialized, 200 lines, 95% precision
class CodeClaimExtractor:      # ✅ Specialized, 180 lines, 85% precision
class ClaimDatabaseMerger:     # ✅ Integration, 100 lines, conflict resolution
```

---

## Tool 1: Formal Mathematical Claim Extractor

### **Technical Specification**

**File:** `.dev_tools/claim_extraction/formal_extractor.py`
**Lines of Code:** ~250
**Dependencies:** `re`, `pathlib`, `dataclasses`, `json`
**Execution Time:** ~1.4 seconds for 259 markdown files

### **Extraction Strategy**

#### **Pass 1: High-Precision Structural Patterns**

```python
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FormalClaim:
    id: str
    type: str  # "theorem", "lemma", "proposition", "corollary"
    number: Optional[int]
    statement: str
    proof: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    confidence: float

class FormalClaimExtractor:
    PATTERNS = {
        'theorem_numbered': re.compile(
            r'\*\*(?P<type>Theorem|Lemma|Proposition|Corollary)\s+(?P<number>\d+)\*\*'
            r'(?:\s*\((?P<title>[^)]+)\))?'  # Optional title
            r'(?:\s*\{cite\}`(?P<cite>[^`]+)`)?'  # Existing citation
            r'\s*(?P<statement>.*?)'  # Statement text
            r'(?=\n\n|\*\*Proof)',  # Stop at proof or blank line
            re.DOTALL | re.MULTILINE
        ),
        'proof_block': re.compile(
            r'\*\*Proof\*\*:?\s*(?P<proof>.*?)(?P<qed>□|∎|QED)',
            re.DOTALL
        ),
        'math_block': re.compile(r'```\{math\}.*?```', re.DOTALL)
    }

    def extract_from_file(self, file_path: Path) -> List[FormalClaim]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        claims = []
        for match in self.PATTERNS['theorem_numbered'].finditer(content):
            claim = FormalClaim(
                id=f"FORMAL-{match.group('type').upper()}-{len(claims)+1:03d}",
                type=match.group('type').lower(),
                number=int(match.group('number')) if match.group('number') else None,
                statement=match.group('statement').strip(),
                proof=self._find_proof_after(content, match.end()),
                file_path=str(file_path),
                line_number=content[:match.start()].count('\n') + 1,
                has_citation=bool(match.group('cite')),
                confidence=self._calculate_confidence(match)
            )
            claims.append(claim)

        return claims

    def _calculate_confidence(self, match) -> float:
        score = 0.5  # Base for pattern match
        if match.group('number'): score += 0.2  # Numbered
        if match.group('cite'): score += 0.2    # Already cited
        # Additional logic for proof, math blocks...
        return min(score, 1.0)
```

#### **Confidence Scoring Algorithm**

```python
# example-metadata:
# runnable: false

def _calculate_confidence(match, has_cite, has_proof, has_math):
    """
    Calculate extraction confidence [0, 1].

    Boosters (cumulative):
    - Numbered (e.g., "Theorem 1"): +0.2
    - Has citation {cite}: +0.2
    - Has proof block: +0.1
    - Has LaTeX math: +0.1

    Expected distribution:
    - High (0.8-1.0): 60% of formal claims
    - Medium (0.5-0.8): 35%
    - Low (0.0-0.5): 5% (manual review)
    """
    score = 0.5
    if match.group('number'): score += 0.2
    if has_cite: score += 0.2
    if has_proof: score += 0.1
    if has_math: score += 0.1
    return min(max(score, 0.0), 1.0)
```

### **Data Model**

```python
# example-metadata:
# runnable: false

@dataclass
class FormalClaim:
    # Identity
    id: str                    # "FORMAL-THEOREM-001"
    type: str                  # "theorem", "lemma", "proposition"
    number: Optional[int]      # Theorem number (if numbered)

    # Content
    statement: str             # Full theorem statement
    proof: Optional[str]       # Associated proof (if found)
    math_blocks: List[str]     # Extracted LaTeX math

    # Location
    file_path: str             # Relative path from project root
    line_number: int           # Line where claim starts
    section_header: str        # Containing section (e.g., "Super-Twisting Algorithm")

    # Context (for AI research)
    context_before: List[str]  # 5 lines before
    context_after: List[str]   # 5 lines after

    # Metadata
    has_citation: bool         # Already has {cite}?
    confidence: float          # Extraction confidence [0, 1]
    suggested_keywords: List[str]  # For AI research queries
```

### **Expected Output**

**File:** `artifacts/formal_claims.json`

```json
{
  "metadata": {
    "total_claims": 41,
    "cited": 12,
    "uncited": 29,
    "by_type": {
      "theorem": 15,
      "lemma": 8,
      "proposition": 12,
      "corollary": 6
    }
  },
  "claims": [
    {
      "id": "FORMAL-THEOREM-001",
      "type": "theorem",
      "number": 1,
      "statement": "The super-twisting algorithm guarantees finite-time convergence...",
      "proof": "Following Moreno and Osorio (2012)...",
      "file_path": "docs/theory/smc_theory_complete.md",
      "line_number": 145,
      "has_citation": false,
      "confidence": 0.95,
      "suggested_keywords": ["super-twisting", "Levant", "Moreno"]
    }
  ]
}
```

### **Unit Tests**

```python
# example-metadata:
# runnable: false

def test_extract_numbered_theorem():
    text = """
    **Theorem 1** (Convergence)

    The system converges in finite time.

    **Proof**: Trivial. □
    """

    claims = extractor.extract_from_text(text)

    assert len(claims) == 1
    assert claims[0].type == "theorem"
    assert claims[0].number == 1
    assert claims[0].proof is not None
    assert claims[0].confidence >= 0.8

def test_citation_detection():
    text = """
    **Theorem 2** {cite}`levant2003higher`

    Super-twisting guarantees convergence.
    """

    claims = extractor.extract_from_text(text)
    assert claims[0].has_citation == True
    assert claims[0].confidence >= 0.9
```

---

## Tool 2: Code Implementation Claim Extractor

### **Technical Specification**

**File:** `.dev_tools/claim_extraction/code_extractor.py`
**Lines of Code:** ~280
**Dependencies:** `ast`, `re`, `pathlib`, `dataclasses`, `json`
**Execution Time:** ~2.5 seconds for 165 Python files

### **Extraction Strategy: AST Traversal**

#### **Why AST Over Pure Regex?**

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Pure Regex** | Fast | Breaks on nested syntax | ❌ |
| **AST Traversal** | Accurate scope | Slower | ✅ **Chosen** |

```python
import ast

class CodeClaimExtractor(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.claims = []
        self.current_scope = []  # Stack: ["module", "class:ClassName", "function:method"]

    def visit_Module(self, node: ast.Module):
        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_from_docstring(docstring, "module", 1)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_scope.append(f"class:{node.name}")
        docstring = ast.get_docstring(node)
        if docstring:
            scope = ':'.join(self.current_scope)
            self._extract_from_docstring(docstring, scope, node.lineno)
        self.generic_visit(node)
        self.current_scope.pop()

    def _extract_from_docstring(self, docstring: str, scope: str, line: int):
        # Pattern matching for implementation claims
        for match in self.PATTERNS['implements'].finditer(docstring):
            claim = CodeClaim(
                id=f"CODE-IMPL-{len(self.claims)+1:03d}",
                algorithm_name=match.group('what').strip(),
                source_attribution=match.group('source').strip(),
                scope=scope,
                file_path=str(self.file_path),
                line_number=line,
                has_citation=self._has_proper_citation(docstring),
                confidence=0.8
            )
            self.claims.append(claim)
```

#### **Citation Pattern Detection**

```python
# example-metadata:
# runnable: false

PATTERNS = {
    'implements': re.compile(
        r'(?:Implements?|Implementation of|Based on)\s+'
        r'(?P<what>[^,\.]+?)\s+'
        r'(?:from|in|by)\s+'
        r'(?P<source>[^\.\n]+)',
        re.IGNORECASE
    ),
    'numbered_cite': re.compile(r'\[(\d+)\]'),
    'doi': re.compile(r'(?:doi:|https://doi\.org/)([^\s]+)', re.IGNORECASE),
    'author_year': re.compile(r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?)\s+(\d{4})\)')
}
```

**Examples Matched:**
- "Implements super-twisting algorithm from Levant 2003" ✅
- "Based on boundary layer technique in Slotine 1991" ✅
- "DOI: 10.1109/TAC.2012.2186179" ✅
- "(Moreno et al. 2012)" ✅

### **Data Model**

```python
# example-metadata:
# runnable: false

@dataclass
class CodeClaim:
    id: str
    type: str  # "implementation", "doi_reference", "algorithm_reference"
    scope: str  # "module" | "class:ClassName" | "function:method_name"
    claim_text: str
    algorithm_name: Optional[str]
    source_attribution: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    citation_format: Optional[str]  # "numbered", "doi", "author_year", "none"
    confidence: float
```

### **Expected Output**

**File:** `artifacts/code_claims.json`

```json
{
  "metadata": {
    "total_claims": 203,
    "cited": 67,
    "by_format": {
      "numbered": 45,
      "doi": 18,
      "author_year": 4,
      "none": 136
    }
  },
  "claims": [
    {
      "id": "CODE-IMPL-042",
      "type": "implementation",
      "scope": "class:ClassicalSMC:function:__init__",
      "algorithm_name": "Matrix regularization",
      "source_attribution": "Leung and colleagues",
      "file_path": "src/controllers/smc/classic_smc.py",
      "line_number": 57,
      "has_citation": false,
      "confidence": 0.75
    }
  ]
}
```

---

## Tool 3: Claims Database Merger

### **Technical Specification**

**File:** `.dev_tools/claim_extraction/merge_claims.py`
**Lines of Code:** ~150
**Execution Time:** <0.5 seconds

### **Merge Strategy**

#### **1. Load Both Extractors' Outputs**

```python
def merge_claims():
    formal = json.load(open('artifacts/formal_claims.json'))
    code = json.load(open('artifacts/code_claims.json'))

    all_claims = formal['claims'] + code['claims']
```

#### **2. Assign Priorities**

```python
# example-metadata:
# runnable: false

def assign_priority(claim: Dict) -> str:
    """
    CRITICAL: Uncited formal theorems/lemmas (scientific risk)
    HIGH: Uncited implementation claims (reproducibility risk)
    MEDIUM: Already cited OR informal claims
    """

    if (claim.get('category') == 'theoretical' and
        claim.get('type') in ['theorem', 'lemma', 'proposition'] and
        not claim.get('has_citation')):
        return 'CRITICAL'  # ~29 claims

    if (claim.get('category') == 'implementation' and
        not claim.get('has_citation')):
        return 'HIGH'  # ~136 claims

    return 'MEDIUM'  # ~335 claims
```

**Expected Priority Distribution:**
```
CRITICAL: 29 claims (5.8%)   → Research first
HIGH: 136 claims (27.2%)     → Research second
MEDIUM: 335 claims (67.0%)   → Research last
```

#### **3. Deduplication with Fuzzy Matching**

```python
# example-metadata:
# runnable: false

def deduplicate_claims(claims: List[Dict]) -> List[Dict]:
    """
    Remove near-duplicates using Jaccard similarity.

    Strategy:
    1. Generate signature from key terms
    2. Compare pairwise (Jaccard similarity)
    3. Merge if similarity > 0.8
    4. Keep higher-confidence version
    """

    deduplicated = []

    for claim in claims:
        signature = _generate_signature(claim)

        # Check against existing
        is_duplicate = False
        for existing in deduplicated:
            similarity = _calculate_similarity(claim, existing)

            if similarity > 0.8:
                is_duplicate = True
                if claim['confidence'] > existing['confidence']:
                    deduplicated.remove(existing)
                    deduplicated.append(claim)
                break

        if not is_duplicate:
            deduplicated.append(claim)

    return deduplicated

def _generate_signature(claim: Dict) -> str:
    """Extract key technical terms (sorted for consistency)."""
    text = claim.get('claim_text', claim.get('statement', ''))
    terms = [w.lower() for w in text.split() if len(w) > 3]
    return '|'.join(sorted(set(terms[:10])))

def _calculate_similarity(claim1: Dict, claim2: Dict) -> float:
    """Jaccard similarity of key terms."""
    sig1 = set(_generate_signature(claim1).split('|'))
    sig2 = set(_generate_signature(claim2).split('|'))
    intersection = sig1 & sig2
    union = sig1 | sig2
    return len(intersection) / len(union) if union else 0.0
```

### **Expected Output**

**File:** `artifacts/claims_inventory.json`

```json
{
  "metadata": {
    "total_claims": 500,
    "sources": {
      "formal_extractor": 41,
      "code_extractor": 203,
      "duplicates_removed": 12
    },
    "by_priority": {
      "CRITICAL": 29,
      "HIGH": 136,
      "MEDIUM": 335
    },
    "citation_status": {
      "cited": 79,
      "uncited": 421,
      "coverage": "15.8%"
    }
  },

  "research_queue": {
    "CRITICAL": ["FORMAL-THEOREM-001", "FORMAL-LEMMA-003", ...],
    "HIGH": ["CODE-IMPL-042", "CODE-IMPL-108", ...],
    "MEDIUM": [...]
  }
}
```

---

## Validation Strategy

### **Unit Tests**

```bash
pytest .dev_tools/claim_extraction/tests/ -v
```

**Test Coverage:**
- Formal extractor: 12 test cases (numbered, unnumbered, with/without proofs)
- Code extractor: 10 test cases (different docstring styles, citation formats)
- Merger: 6 test cases (deduplication, priority assignment)

### **Integration Test**

```bash
python .dev_tools/claim_extraction/formal_extractor.py
python .dev_tools/claim_extraction/code_extractor.py
python .dev_tools/claim_extraction/merge_claims.py
```

**Expected Output:**
```
✓ smc_theory_complete.md: 9 claims
✓ pso_optimization_complete.md: 8 claims
...
📊 Extracted 41 formal claims
   Cited: 12, Uncited: 29

✓ classic_smc.py: 3 claims
✓ sta_smc.py: 4 claims
...
📊 Extracted 203 code claims
   Cited: 67, Uncited: 136

✅ Merged 500 total claims
   CRITICAL: 29, HIGH: 136, MEDIUM: 335
```

### **Manual Validation**

**Sample 40 random claims (stratified by priority):**
- 10 CRITICAL (expected precision: ≥95%)
- 15 HIGH (expected precision: ≥85%)
- 15 MEDIUM (expected precision: ≥80%)

**Acceptance Criteria:**
- ✅ ≥90% precision overall (36/40 correct)
- ✅ ≥95% recall on ground truth files

---

## Timeline & Milestones

### **Week 1: Tool Development**

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| **Mon** | Formal extractor: Regex patterns | 3 | `formal_extractor.py` v0.1 |
| **Tue** | Formal extractor: Proof association | 3 | `formal_extractor.py` v1.0 |
| **Wed** | Formal extractor: Testing | 2 | Unit tests passing |
| **Thu** | Code extractor: AST visitor | 3 | `code_extractor.py` v0.1 |
| **Fri** | Code extractor: Citation detection | 3 | `code_extractor.py` v1.0 |
| **Total** | | **14 hrs** | **2 extractors ready** |

### **Week 2: Integration & Validation**

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| **Mon** | Database merger implementation | 2 | `merge_claims.py` v1.0 |
| **Tue** | Full extraction run | 2 | `claims_inventory.json` |
| **Wed** | Quality report generation | 1 | `extraction_quality_report.html` |
| **Thu** | Manual verification (40 claims) | 2 | Validated claims list |
| **Fri** | Documentation + handoff | 1 | Phase 1 complete ✅ |
| **Total** | | **8 hrs** | **Phase 1 deliverables** |

**Grand Total:** 22 hours (within 15-20 hour estimate + 2-hour buffer)

---

## Success Criteria (Acceptance Gates)

### **Mandatory Gates** ✅

- ✅ **Extraction Count**: ≥500 total claims extracted
- ✅ **CRITICAL Claims**: ≥25 uncited formal theorems identified
- ✅ **Precision**: ≥90% on manual review sample (40 claims)
- ✅ **Recall**: ≥95% on ground truth files
- ✅ **Performance**: <5 seconds total execution time
- ✅ **JSON Schema**: All outputs validate against schema

### **Quality Gates** (Should Pass)

- ✅ **High Confidence**: ≥60% of claims with confidence >0.8
- ✅ **Deduplication**: <5% duplicate claims removed
- ✅ **Coverage**: 100% of markdown and Python files analyzed

---

## Artifacts Delivered to Phase 2

```
.dev_tools/claim_extraction/
├── formal_extractor.py       # 250 lines, tested
├── code_extractor.py         # 280 lines, tested
├── merge_claims.py           # 150 lines, tested
└── tests/                    # Unit tests

artifacts/
├── formal_claims.json        # 41 formal claims
├── code_claims.json          # 203 code claims
├── claims_inventory.json     # 500 unified claims
└── extraction_quality_report.html

Interface to Phase 2:
└── Research Queue: CRITICAL → HIGH → MEDIUM
    └── Expected: 29 CRITICAL claims researched first
```

---

**Related Documents:**
- [00_master_roadmap.md](00_master_roadmap.md) - Complete 5-phase plan
- [01_initial_analysis.md](01_initial_analysis.md) - Problem analysis
- [03_phase2_ai_research.md](03_phase2_ai_research.md) - Next phase *(to be created)*

**Status:** ✅ **READY FOR IMPLEMENTATION**

**End of Phase 1 Plan**
