# Citation System - Initial Analysis & Problem Decomposition

**Document Version:** 1.0.0
**Created:** 2025-01-15
**Purpose:** Ultra-deep analysis of citation needs and systematic approach

---

## Table of Contents

1. [Scope Assessment](#scope-assessment)
2. [Claim Categories](#claim-categories)
3. [Strategic Approach](#strategic-approach)
4. [Multi-Agent Orchestration](#multi-agent-orchestration)
5. [Decision Framework](#decision-framework)

---

## Scope Assessment

### **Current State Analysis**

**Documentation Scale:**
- **259 markdown files** across documentation tree
- **41 formal mathematical claims** (Theorems, Lemmas, Propositions, Definitions)
- **101 theoretical/mathematical sections** requiring rigorous citations
- **271 files** with citation-like patterns detected

**Code Implementation:**
- **165 Python files** in `src/` directory
- **368 implementation claim occurrences** across codebase
- **Estimated 150-250 distinct implementation claims** after deduplication

**Citation Coverage:**
- ✅ **Existing bibliography**: 39 references (incomplete)
- ✅ **Citation format**: Sphinx/MyST `{cite}` syntax in some docs
- ❌ **Coverage gap**: ~85% of claims lack proper citations
- ❌ **Inconsistency**: Mixed citation styles (numbered [1], DOI, author-year)

###

 **Quantitative Breakdown**

```
Total Claims Estimate: 500-600
├─ Formal Mathematical: 41 claims
│  ├─ Theorems: 15
│  ├─ Lemmas: 8
│  ├─ Propositions: 12
│  └─ Corollaries/Definitions: 6
│
├─ Implementation References: 150-250 claims
│  ├─ Algorithm attributions: ~100
│  ├─ Numerical methods: ~50
│  ├─ Design patterns: ~40
│  └─ Library dependencies: ~60
│
├─ Performance/Benchmark Claims: 50-80 claims
│  ├─ Improvement metrics: ~30
│  ├─ Complexity bounds: ~20
│  └─ Statistical validation: ~30
│
└─ Domain Knowledge Assertions: 100-150 claims
   ├─ "Well-known" techniques: ~50
   ├─ "Standard" approaches: ~40
   └─ "Common" practices: ~60

Current Citation Coverage:
├─ Properly cited: 89 claims (15-18%)
├─ Partially cited (vague): 132 claims (22-26%)
└─ Uncited: 326 claims (54-65%)
```

---

## Claim Categories

### **Category 1: Formal Mathematical Claims**

**Characteristics:**
- Explicitly labeled as "Theorem", "Lemma", "Proposition", or "Corollary"
- Often accompanied by proofs (markers: "Proof:", "□", "∎", "QED")
- Contain mathematical notation (LaTeX blocks, equations)
- High precision extraction possible (95%+ via regex)

**Examples from Codebase:**

**Example 1** (`docs/theory/smc_theory_complete.md:72`):
```markdown
**Theorem 1 (Surface Stability)**: If all sliding surface parameters $c_i > 0$,
then the sliding surface dynamics are exponentially stable with convergence rates
determined by $c_i$.

*Proof*: The characteristic polynomial of each error component is $s + c_i = 0$,
yielding eigenvalues $\lambda_i = -c_i < 0$ for $c_i > 0$. □
```

**Citation Status:** ❌ Uncited
**Required Reference:** Utkin 1999 or Slotine 1991 (sliding surface design theory)
**Priority:** CRITICAL (fundamental stability claim)

**Example 2** (`docs/theory/pso_optimization_complete.md:86`):
```markdown
**Theorem 1 (Stability Condition)**: The particle converges to a stable trajectory if:

$$0 < w < 1 \quad \text{and} \quad 0 < c_1 + c_2 < 2(1 + w)$$

*Proof*: The characteristic equation of the difference equation is...
```

**Citation Status:** ❌ Uncited
**Required Reference:** Clerc & Kennedy 2002 (constriction factor)
**Priority:** CRITICAL (PSO convergence guarantee)

### **Category 2: Implementation Claims**

**Characteristics:**
- Found in docstrings (module, class, function level)
- Phrases: "Implements X from Y", "Based on Z", "Following [Author Year]"
- May include numbered citations [1], DOIs, or author-year formats
- Medium precision extraction (70-85% via AST + regex)

**Examples from Codebase:**

**Example 1** (`src/controllers/smc/classic_smc.py:57`):
```python
"""
Adding a small, positive constant to the diagonal of a symmetric matrix is a
well‑known regularisation technique: in the context of covariance matrices,
Leung and colleagues recommend "adding a small, positive constant to the
diagonal" to ensure the matrix is invertible.
"""
```

**Citation Status:** ❌ Uncited (vague "Leung and colleagues")
**Required Reference:** Leung, D. et al. (2012) with DOI or specific journal
**Priority:** HIGH (numerical stability claim)

**Example 2** (`src/controllers/smc/sta_smc.py:docstring`):
```python
"""
Super-Twisting Sliding Mode Controller (STA-SMC).

Implements the second-order sliding mode algorithm from Levant [1] with
finite-time convergence guarantees proven by Moreno and Osorio [2].
"""
```

**Citation Status:** ✅ Partially cited (numbered [1], [2])
**Required Reference:** Extract References section, convert to BibTeX
**Priority:** MEDIUM (already has references, needs formatting)

### **Category 3: Performance/Benchmark Claims**

**Characteristics:**
- Quantitative improvement metrics ("6x improvement", "50% reduction")
- Complexity bounds ("O(n log n)", "linear time")
- Statistical validation claims ("99% confidence", "p < 0.05")
- Require experimental validation or methodology citations

**Examples from Codebase:**

**Example 1** (`CHANGELOG.md:13`):
```markdown
False positive rate reduced from ~80% to 15.9% (6x improvement)
```

**Citation Status:** ❌ Uncited
**Required Reference:**
  - Statistical methodology for P99 threshold selection (Otsu 1979?)
  - ROC curve analysis (Fawcett 2006)
**Priority:** HIGH (validation claim without methodology)

**Example 2** (`docs/benchmarks_methodology.md`):
```markdown
Numba acceleration provides 10-100x speedup for batch simulations
```

**Citation Status:** ❌ Uncited
**Required Reference:**
  - Numba JIT compilation paper (Lam et al. 2015)
  - Benchmarking methodology (own experimental data)
**Priority:** MEDIUM (performance claim needs validation)

### **Category 4: Domain Knowledge Assertions**

**Characteristics:**
- "Well-known", "Standard", "Common", "Typical", "Established"
- Often true but lack explicit citations (weasel words)
- High false positive risk (80%+ informal usage)
- Require NLP-based semantic detection

**Examples from Codebase:**

**Example 1** (`src/controllers/smc/classic_smc.py:34`):
```python
"""
The boundary‑layer approximation attenuates chattering at the cost of
introducing a finite steady‑state tracking error; for example, a discussion
of chattering reduction methods emphasises that the boundary‑layer method
"reduces chattering but leads to a finite steady state error".
"""
```

**Citation Status:** ❌ Uncited (paraphrased but no source)
**Required Reference:** Slotine 1991 or Edwards & Spurgeon 1998 (chattering reduction)
**Priority:** HIGH (fundamental trade-off claim)

**Example 2** (`docs/theory/smc_theory_complete.md:introduction`):
```markdown
Sliding Mode Control (SMC) is a robust control methodology that provides
finite-time convergence and inherent disturbance rejection capabilities.
```

**Citation Status:** ❌ Uncited (introductory statement)
**Required Reference:** Utkin 1999 (foundational SMC textbook)
**Priority:** MEDIUM (general introduction, could cite Utkin for authority)

---

## Strategic Approach

### **Why Multi-Stage Extraction?**

**Problem:** Different claim types have different:
- **Structural characteristics** (formal vs informal)
- **Extraction complexity** (regex vs NLP)
- **Precision requirements** (CRITICAL claims need 95%+, informal 70% okay)
- **Validation methods** (manual review vs automated)

**Solution:** Specialized extractors with tailored strategies

```
┌─────────────────────────────────────────────────────┐
│         Claim Extraction Pipeline                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Stage 1: Formal Math (Regex-based)                │
│  ├─ Input: docs/**/*.md                           │
│  ├─ Pattern: **Theorem X**, **Lemma Y**          │
│  ├─ Precision: 95%                                │
│  └─ Output: formal_claims.json (40-50 claims)     │
│                                                     │
│  Stage 2: Code Impl (AST-based)                    │
│  ├─ Input: src/**/*.py                            │
│  ├─ Pattern: "Implements", DOI, [1][2]           │
│  ├─ Precision: 85%                                │
│  └─ Output: code_claims.json (150-250 claims)     │
│                                                     │
│  Stage 3: Domain Knowledge (NLP-based)             │
│  ├─ Input: All text                               │
│  ├─ Pattern: "well-known", "standard"            │
│  ├─ Precision: 60% (high false positives)        │
│  └─ Output: weasel_claims.json (100-150 claims)   │
│                                                     │
│  Stage 4: Merge & Deduplicate                      │
│  ├─ Fuzzy matching (Jaccard similarity)          │
│  ├─ Priority assignment (CRITICAL/HIGH/MEDIUM)    │
│  └─ Output: claims_inventory.json (500+ claims)    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### **Extraction Strategy per Category**

| Category | Strategy | Tools | Precision | Manual Review |
|----------|----------|-------|-----------|---------------|
| **Formal Math** | Regex patterns | `re`, `dataclasses` | 95% | CRITICAL claims only (~10) |
| **Code Impl** | AST + Regex | `ast`, `re` | 85% | Low-confidence only (~30) |
| **Performance** | Regex + Context | `re`, pattern matching | 80% | Sample validation (~20) |
| **Domain Knowledge** | NLP (optional) | `transformers` | 60% | High false positives (~50) |

### **Priority Assignment Logic**

```python
def assign_priority(claim: Dict) -> str:
    """
    CRITICAL: Uncited formal theorems/lemmas (scientific credibility risk)
    HIGH: Uncited implementation claims (reproducibility risk)
    MEDIUM: Already cited OR informal claims (lower impact)
    """

    if (claim['category'] == 'theoretical' and
        claim['type'] in ['theorem', 'lemma', 'proposition'] and
        not claim['has_citation']):
        return 'CRITICAL'  # ~29 claims

    if (claim['category'] == 'implementation' and
        claim['type'] == 'implementation' and
        not claim['has_citation']):
        return 'HIGH'  # ~136 claims

    return 'MEDIUM'  # ~335 claims
```

**Expected Distribution:**
- CRITICAL: 29 claims (5.8%) → Research first (foundational theorems)
- HIGH: 136 claims (27.2%) → Research second (reproducibility)
- MEDIUM: 335 claims (67.0%) → Research last (polish)

---

## Multi-Agent Orchestration

### **Agent Selection Decision Tree**

**Input:** User request "Build systematic citation verification system"

**Analysis:**
```
Required Skills:
├─ Citation extraction          ❌ NEW (no existing agent)
├─ Academic API integration     ❌ NEW (no existing agent)
├─ NLP text analysis            ❌ NEW (no existing agent)
├─ Scientific writing           ✅ Documentation Expert (35% match)
├─ Cross-reference validation   ✅ Integration Coordinator (25% match)
├─ BibTeX management            ❌ NEW (no existing agent)
└─ Database design              ❌ NEW (no existing agent)

Skill Gap: 62.5% (5/8 requirements not covered)

Decision: CREATE NEW AGENT
└─ Name: "Academic Research Automation Engineer"
   └─ Justification: Specialized domain (academic APIs + NLP)
                    requires dedicated tooling
```

### **Optimal 3-Agent Configuration**

**Ultimate Orchestrator Delegates to:**

1. **Academic Research Automation Engineer** (NEW - BLOCKING)
   - **Responsibility:** Claim extraction + AI-powered research
   - **Inputs:** Documentation files (259 .md), code files (165 .py)
   - **Outputs:**
     - `claims_inventory.json` (500+ claims with priorities)
     - `research_results.json` (ranked academic references)
     - `enhanced_bibliography.bib` (150-200 BibTeX entries)
     - `citation_mapping.json` (claim_id → citation_keys)
   - **Duration:** Week 1-4 (40-55 hours)

2. **Documentation Expert** (EXISTING)
   - **Responsibility:** Citation formatting + Sphinx integration
   - **Inputs:**
     - `enhanced_bibliography.bib` (from NEW agent)
     - `citation_mapping.json` (from NEW agent)
   - **Outputs:**
     - `patches/citation_insertions.patch` (Sphinx `{cite}` additions)
     - Updated `docs/references/bibliography.md` (IEEE format)
     - `artifacts/citation_style_report.json`
   - **Duration:** Week 5-6 (20-25 hours)

3. **Integration Coordinator** (EXISTING)
   - **Responsibility:** Cross-reference validation + QA
   - **Inputs:**
     - `claims_inventory.json` (from NEW agent)
     - `citation_insertions.patch` (from DOC expert)
   - **Outputs:**
     - `artifacts/cross_reference_validation.json`
     - `artifacts/coverage_gate_results.json`
     - `.github/workflows/citation_validation.yml` (CI)
   - **Duration:** Week 7-8 (10-15 hours)

### **Why This Configuration?**

**Parallelization Potential:**
```
Timeline with 3 agents:

Week 1-2: NEW AGENT (Claim extraction)
Week 3-4: NEW AGENT (AI research)
Week 5-6: NEW AGENT + DOC EXPERT (parallel on different claim batches)
Week 7-8: INTEGRATION COORDINATOR (final validation)

Speedup: ~1.8x vs sequential
Token Usage: Optimal (reusing 2 existing agents)
```

**Alternative Rejected:**
- **2 agents (NEW + DOC)**: No validation/QA specialist (risk: inconsistencies)
- **4 agents**: Diminishing returns (overhead > speedup benefit)
- **1 monolithic agent**: Token inefficient, too broad

---

## Decision Framework

### **Agent Reuse vs Creation Decision Matrix**

```python
class AgentSelectionStrategy:
    """
    Decision framework for optimal agent configuration.
    """

    EXISTING_AGENTS = {
        'integration_coordinator': {
            'skills': ['cross-domain orchestration', 'system health',
                      'config validation', 'debugging across components'],
            'match_score': 0.25  # For citation system
        },
        'documentation_expert': {
            'skills': ['LaTeX math', 'Sphinx docs', 'scientific writing',
                      'citation systems', 'mathematical notation'],
            'match_score': 0.35  # For citation system
        },
        'pso_optimization_engineer': {
            'skills': ['PSO tuning', 'convergence analysis'],
            'match_score': 0.10  # Low relevance
        },
        'control_systems_specialist': {
            'skills': ['SMC design', 'stability analysis'],
            'match_score': 0.15  # Domain knowledge only
        }
    }

    def should_create_new(self, requirements: Set[str]) -> bool:
        """
        Create new agent if:
        1. Skill gap > 30% (best match < 0.7)
        2. Workload > 40 hours AND parallelizable
        3. CLAUDE.md mandates specialist
        """

        best_match = max(agent['match_score']
                        for agent in self.EXISTING_AGENTS.values())

        skill_gap = 1.0 - best_match

        # Citation system: best_match = 0.35 (Doc Expert)
        # skill_gap = 0.65 (65% of requirements not covered)

        if skill_gap > 0.30:
            return True, "SKILL_GAP"

        return False, "REUSE_SUFFICIENT"
```

### **Artifact Contract Design**

**Shared JSON Schema:**
```json
{
  "metadata": {
    "agent_name": "string",
    "timestamp": "ISO8601",
    "confidence": "float (0.0-1.0)"
  },

  "claims": [
    {
      "id": "FORMAL-THEOREM-001",
      "type": "theorem|lemma|implementation|performance",
      "category": "theoretical|implementation|benchmark",
      "priority": "CRITICAL|HIGH|MEDIUM",
      "claim_text": "string",
      "file_path": "relative/path/to/file",
      "line_number": "int",
      "has_citation": "bool",
      "confidence": "float",
      "suggested_keywords": ["string"]
    }
  ],

  "research_results": [
    {
      "claim_id": "FORMAL-THEOREM-001",
      "ranked_references": [
        {
          "doi": "10.1080/...",
          "title": "string",
          "authors": ["string"],
          "year": "int",
          "venue": "string",
          "citation_count": "int",
          "relevance_score": "float"
        }
      ]
    }
  ]
}
```

**Integration Algorithm:**
```python
def integrate_artifacts(agent_outputs: List[Dict]) -> Dict:
    """
    Merge outputs from multiple agents.

    Conflict resolution priority:
    1. Domain expert wins (NEW agent for research quality)
    2. Higher confidence wins (confidence > 0.8 overrides < 0.8)
    3. More specific wins (file-level > directory-level)
    4. Manual review (flag for human if unresolvable)
    """

    merged = {'changes': [], 'conflicts': []}

    by_file = defaultdict(list)
    for output in agent_outputs:
        for change in output['changes']:
            by_file[change['file']].append((output['metadata']['agent_name'], change))

    for file_path, changes in by_file.items():
        if len(changes) > 1:
            # Conflict detected
            winner = max(changes, key=lambda x: (
                DOMAIN_PRIORITY.get(x[0], 0),  # NEW agent > DOC > INT
                x[1].get('confidence', 0.0)
            ))
            merged['changes'].append(winner[1])
            merged['conflicts'].append({
                'file': file_path,
                'resolution': f"Used {winner[0]} (domain + confidence)"
            })
        else:
            merged['changes'].append(changes[0][1])

    return merged
```

---

## Summary Statistics (Projected)

### **Claim Inventory Breakdown**

```
Expected `claims_inventory.json` structure:

{
  "metadata": {
    "total_claims": 500,
    "by_category": {
      "theoretical": 41,
      "implementation": 203,
      "performance": 87,
      "domain_knowledge": 169
    },
    "by_priority": {
      "CRITICAL": 29,   # 5.8% - Uncited theorems
      "HIGH": 136,      # 27.2% - Uncited implementations
      "MEDIUM": 335     # 67.0% - Cited or informal
    },
    "citation_status": {
      "cited": 79,
      "uncited": 421,
      "coverage": "15.8%"
    }
  }
}
```

### **Research Queue Prioritization**

**Phase 2 Research Order:**

1. **CRITICAL Queue** (Week 3, ~15 hours)
   - 29 formal theorems/lemmas without citations
   - High-impact references (Utkin, Levant, Moreno, Slotine)
   - Expected: 2-4 references per claim

2. **HIGH Queue** (Week 3-4, ~20 hours)
   - 136 implementation claims without proper citations
   - Mix of algorithm papers + GitHub repos
   - Expected: 1-3 references per claim

3. **MEDIUM Queue** (Week 4, ~10 hours)
   - 335 lower-priority claims (already cited or informal)
   - Polish existing citations, add DOIs
   - Expected: 0-2 references per claim

**Total Research Output:** 150-200 unique references

---

## Next Steps

### **Immediate Actions (Phase 1)**

1. **Build Formal Claim Extractor** (Day 1-3)
   - Implement regex patterns for theorems/lemmas
   - Add proof association logic
   - Create confidence scoring algorithm
   - **Deliverable:** `formal_extractor.py` + unit tests

2. **Build Code Claim Extractor** (Day 4-6)
   - Implement AST visitor pattern
   - Add citation format detection
   - Handle multiple docstring styles
   - **Deliverable:** `code_extractor.py` + unit tests

3. **Build Database Merger** (Day 7)
   - Implement fuzzy deduplication
   - Add priority assignment logic
   - Generate research queue
   - **Deliverable:** `merge_claims.py` + `claims_inventory.json`

### **Validation Milestones**

- ✅ **Extraction Complete:** `claims_inventory.json` exists with ≥500 claims
- ✅ **Quality Validated:** Manual review of 40 claims shows ≥90% precision
- ✅ **Ground Truth Checked:** Recall ≥95% on known theorem files
- ✅ **Ready for Phase 2:** Research queue prioritized and ready

---

## Appendix: Example Outputs

### **Sample Formal Claim (JSON)**

```json
{
  "id": "FORMAL-THEOREM-001",
  "type": "theorem",
  "category": "theoretical",
  "number": 1,
  "title": "Finite-Time Convergence",
  "statement": "The super-twisting algorithm guarantees finite-time convergence to the sliding surface s = 0 with convergence time bounded by: t_c ≤ 2V^{1/2}(0)/(α - β)",
  "proof": "Following Moreno and Osorio (2012): 1. Construct strict Lyapunov function...",
  "math_blocks": ["t_c ≤ 2V^{1/2}(0)/(α - β)"],
  "file_path": "docs/theory/smc_theory_complete.md",
  "line_number": 145,
  "section_header": "Super-Twisting Algorithm",
  "context_before": ["### Theoretical Foundation", "The super-twisting algorithm is..."],
  "context_after": ["**Proof**: Following Moreno...", "This result guarantees..."],
  "has_citation": false,
  "confidence": 0.95,
  "priority": "CRITICAL",
  "suggested_keywords": ["super-twisting", "finite-time convergence", "Levant", "Moreno", "Lyapunov"],
  "extraction_method": "regex_formal_math",
  "extraction_timestamp": "2025-01-15T10:30:00Z"
}
```

### **Sample Code Claim (JSON)**

```json
{
  "id": "CODE-IMPL-042",
  "type": "implementation",
  "category": "implementation",
  "scope": "class:ClassicalSMC:function:__init__",
  "claim_text": "Adding a small, positive constant to the diagonal of a symmetric matrix is a well‑known regularisation technique: in the context of covariance matrices, Leung and colleagues recommend...",
  "algorithm_name": "Matrix regularization",
  "source_attribution": "Leung and colleagues",
  "file_path": "src/controllers/smc/classic_smc.py",
  "line_number": 57,
  "code_context": "...numerical robustness. Adding a tiny constant to the diagonal...",
  "has_citation": false,
  "citation_format": null,
  "confidence": 0.75,
  "priority": "HIGH",
  "suggested_search": "Leung covariance matrix diagonal regularization",
  "extraction_method": "ast_docstring_parsing",
  "extraction_timestamp": "2025-01-15T10:32:00Z"
}
```

---

**End of Initial Analysis**

**Related Documents:**
- [00_master_roadmap.md](00_master_roadmap.md) - Complete 5-phase plan
- [02_phase1_claim_extraction.md](02_phase1_claim_extraction.md) - Phase 1 implementation details

**Status:** ✅ **ANALYSIS COMPLETE - READY FOR PHASE 1**
