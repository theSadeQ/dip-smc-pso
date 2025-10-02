# Research Workflow V2 - Citation Quality Assurance

**Version:** 2.0
**Date:** 2025-10-02
**Purpose:** Prevent citation quality issues through systematic verification and proper scope definition
**Replaces:** Original workflow (implicit in RESEARCH_QUICKSTART.md)

---

## Overview

This workflow addresses critical issues identified in Batch 08 where 41.7% of citations were incorrect due to:
1. AI suggestions without source code verification
2. Topic clustering bias (all SMC files → SMC papers, regardless of content)
3. Inappropriate citations for implementation code
4. No quality gates or verification steps

**Key Principle:** **Not all code requires academic citations.** Theory requires citations; implementation patterns often do not.

---

## Workflow Phases

```
Phase 0: Triage → Phase 1: Code Review → Phase 2: Research → Phase 3: Verification → Gate: Approval
```

---

## Phase 0: Pre-Research Triage (NEW - MANDATORY)

**Goal:** Determine which claims actually need academic citations

**Input:** `claims.json` from batch directory
**Output:** `claims_triaged.json` with categories assigned
**Time:** ~30-60 minutes for 300 claims (semi-automated)

### Step 1: Run Automated Triage

```bash
cd .dev_tools
python triage_claims.py --batch 08_HIGH_implementation_general
```

**Tool classifies claims into 4 categories:**

#### Category A: REQUIRES CITATION (Algorithmic Theory)
**Characteristics:**
- Mathematical algorithms (SMC, PSO, numerical integration, differential evolution)
- Statistical methods (cross-validation, bootstrap, hypothesis tests, normality tests)
- Control theory (stability analysis, Lyapunov functions, reaching laws)
- Optimization algorithms (genetic, particle swarm, simplex, gradient-based)
- Signal processing algorithms (FFT, filtering, state estimation)

**Examples:**
- ✅ `compute_lyapunov_function()` → Needs Lyapunov stability citation
- ✅ `k_fold_cross_validation()` → Needs cross-validation citation
- ✅ `bootstrap_confidence_interval()` → Needs bootstrap methods citation
- ✅ `super_twisting_algorithm()` → Needs Levant (2003) citation

**Citation Type:** Peer-reviewed journal articles or seminal conference papers

---

#### Category B: REQUIRES CITATION (Foundational Concepts)
**Characteristics:**
- Performance metrics definitions (ISE, IAE, overshoot, settling time)
- System modeling approaches (state-space, transfer functions)
- Analysis methodologies (frequency response, step response)
- Well-known control strategies (PID, LQR basics)

**Examples:**
- ✅ `compute_overshoot()` → Needs control systems textbook
- ✅ `integral_absolute_error()` → Needs performance metrics reference
- ✅ `state_space_model()` → Needs systems theory reference

**Citation Type:** Authoritative textbooks or standards

---

#### Category C: NO CITATION NEEDED (Pure Implementation)
**Characteristics:**
- Software design patterns (factory, singleton, observer, strategy)
- Initialization code, constructors, destructors, reset methods
- Serialization, deserialization (to_dict, from_dict, JSON parsing)
- Interface definitions, abstract base classes, protocols
- Threading primitives (locks, mutexes, deadlock detection)
- Configuration parsing, file I/O, logging
- Data structures (lists, dictionaries, named tuples)
- Getter/setter methods, property decorators
- Type validation, input sanitization
- Error handling, exception raising

**Examples:**
- ❌ `class ControllerFactory:` → No citation (factory pattern)
- ❌ `def __init__(self, config):` → No citation (constructor)
- ❌ `def to_dict(self):` → No citation (serialization)
- ❌ `def reset_state(self):` → No citation (reset method)
- ❌ `with threading.Lock():` → No citation (concurrency primitive)
- ❌ `@dataclass class Config:` → No citation (data structure)

**Citation:** None required (or optionally cite "Design Patterns" book if policy requires)

---

#### Category D: UNCERTAIN (Manual Review Required)
**Characteristics:**
- Ambiguous descriptions
- Hybrid code (part algorithm, part implementation)
- Novel combinations of existing methods
- Domain-specific adaptations

**Examples:**
- ❓ "Compute adaptive threshold" → Could be novel or standard
- ❓ "Initialize optimization parameters" → Depends on method
- ❓ "Hybrid switching logic" → May need citation if novel

**Action:** Manual source code review to determine A/B/C

---

### Step 2: Manual Review of Triage Results

**Checklist:**
- [ ] Review all Category A claims - verify they're truly algorithmic
- [ ] Review all Category C claims - ensure they're truly implementation-only
- [ ] Manually categorize all Category D claims (read source code)
- [ ] Spot-check random 10% of automated categorizations

**Output:** Finalized `claims_triaged.json`

---

## Phase 1: Human Code Review (MANDATORY)

**Goal:** Verify claim descriptions match actual code before research

**Input:** Claims requiring citation (Category A + B)
**Output:** `claims_verified.json` with code summaries
**Time:** ~5 minutes per claim

### For Each Claim Requiring Citation:

1. **Open source file** at specified line number
2. **Read ±20 lines of context** around the claim
3. **Answer these questions:**
   - What does this code actually do? (1-2 sentences)
   - What algorithm/method is implemented?
   - Is this theory or just implementation scaffolding?
   - Does the claim description accurately reflect the code?

4. **Write verified summary:**
   ```json
   {
     "claim_id": "CODE-IMPL-063",
     "verified_summary": "Implements K-Fold cross-validation splitter. Creates train/test indices for model validation using stratified sampling.",
     "actual_algorithm": "K-Fold Cross-Validation",
     "confidence": "HIGH",
     "needs_citation": true
   }
   ```

5. **Flag mismatches:**
   - If claim says "normality testing" but code is "cross-validation" → Flag for correction
   - If claim is vague but code is specific → Rewrite claim description

**Quality Gate:** Researcher must personally read code. No skipping this step.

---

## Phase 2: Citation Research (Only for Verified A/B Claims)

**Goal:** Find appropriate citations that match actual code

**Input:** `claims_verified.json`
**Output:** Citation suggestions with rationale
**Time:** ~10-15 minutes per unique citation

### Step 1: Use ChatGPT with Verified Summaries

**Prompt Template:**
```
I need a peer-reviewed citation for the following code implementation:

Algorithm: K-Fold Cross-Validation
Description: Implements stratified K-fold splitting for model validation
File: src/analysis/validation/cross_validation.py
Code Context: [paste relevant code snippet]

Requirements:
1. Seminal or widely-cited paper introducing this method
2. Peer-reviewed journal or major conference
3. Must directly describe this specific algorithm/method
4. Include: Title, Authors, Year, Journal, DOI

Do NOT suggest papers that just mention this method in passing.
```

### Step 2: Validate ChatGPT Suggestions

**Validation Checklist:**
- [ ] Paper title/abstract mentions the specific algorithm
- [ ] Publication is peer-reviewed (journal or top-tier conference)
- [ ] DOI resolves and is accessible
- [ ] Year is reasonable (seminal work or standard reference)
- [ ] Not a review paper (unless most appropriate)
- [ ] Citation matches code topic (e.g., not citing PSO for SMC code)

**Red Flags:**
- ❌ Paper title doesn't mention the algorithm at all
- ❌ Citation is a generic textbook chapter
- ❌ Year is too recent (possibly not seminal)
- ❌ Can't access paper to verify relevance
- ❌ Paper is tangentially related (mentions method in one paragraph)

### Step 3: Cross-Reference with Similar Claims

**Check for consistency:**
- If 5 claims use K-Fold cross-validation → All should cite same source
- If claim is similar to existing cited claim → Reuse citation
- If different aspects of same method → Consider multiple citations

---

## Phase 3: Quality Verification (MANDATORY)

**Goal:** Catch mismatches before CSV integration

**Input:** Proposed citations
**Output:** Verification report
**Time:** ~30 minutes for 300 claims (automated)

### Step 1: Automated Verification

```bash
cd .dev_tools
python verify_batch_citations.py --batch 08_HIGH_implementation_general --output verification_report.md
```

**Tool checks:**
- Pattern detection (cross-validation code cited to cross-validation paper?)
- Topic alignment (SMC code → SMC citations, not MPC/PSO)
- Category violations (Category C with citations → Flag)
- Consistency (same algorithm → same citation)

### Step 2: Manual Sample Verification (10% Random)

**Select random 10% of claims:**
```bash
python sample_claims.py --batch 08 --count 30
```

**For each sample:**
1. Read source code
2. Verify citation matches code
3. Check citation is accessible and relevant
4. Document any issues

**Acceptance Criteria:**
- ≥95% of sampled claims correctly cited
- No severe mismatches (control theory for software patterns)
- Citations are accessible and verifiable

### Step 3: Peer Review (Critical Claims Only)

**Identify critical claims:**
- Core algorithm implementations (SMC, PSO, MPC)
- Novel adaptations or combinations
- Safety-critical functions

**Peer review process:**
1. Senior researcher reviews citation appropriateness
2. Verifies citation matches implementation
3. Suggests alternative citations if needed
4. Approves or requests revision

---

## Quality Gates (CANNOT SKIP)

### Gate 1: After Triage
**Criteria:**
- [ ] All claims categorized (A/B/C/D)
- [ ] Category D claims manually reviewed and recategorized
- [ ] Category C claims marked "no citation needed"
- [ ] Triage decisions documented with rationale

**Owner:** Research Lead
**Fail Action:** Complete triage before proceeding

---

### Gate 2: After ChatGPT Suggestions
**Criteria:**
- [ ] All suggestions validated against checklist
- [ ] No topic mismatches (e.g., MPC cited for SMC)
- [ ] All DOIs verified to resolve
- [ ] Citation reuse is logical and consistent

**Owner:** Researcher
**Fail Action:** Revise citations that fail validation

---

### Gate 3: Before CSV Integration
**Criteria:**
- [ ] Automated verification passed (≥95% expected accuracy)
- [ ] Sample verification passed (10% random check)
- [ ] Peer review completed (critical claims)
- [ ] No severe mismatches detected
- [ ] Verification report approved

**Owner:** Research Lead + Peer Reviewer
**Fail Action:** Address flagged issues before CSV update

---

## Tools & Scripts

### 1. Triage Tool
**File:** `.dev_tools/triage_claims.py`
**Purpose:** Automated categorization of claims
**Usage:**
```bash
python triage_claims.py --batch 08_HIGH_implementation_general --output claims_triaged.json
```

### 2. Verification Tool
**File:** `.dev_tools/verify_batch_citations.py`
**Purpose:** Detect citation mismatches
**Usage:**
```bash
python verify_batch_citations.py --batch 08 --output verification_report.md
```

### 3. Sample Selection Tool
**File:** `.dev_tools/sample_claims.py`
**Purpose:** Random sampling for manual verification
**Usage:**
```bash
python sample_claims.py --batch 08 --count 30 --seed 42
```

### 4. Citation Consistency Checker
**File:** `.dev_tools/check_citation_consistency.py`
**Purpose:** Ensure same algorithms cite same sources
**Usage:**
```bash
python check_citation_consistency.py --csv claims_research_tracker.csv
```

---

## Templates

### Code Review Template
```markdown
**Claim ID:** CODE-IMPL-063
**File:** src/analysis/validation/cross_validation.py:1
**Line Range:** 1-30

**What the code does:**
Implements K-Fold cross-validation splitter for model validation.
Creates stratified train/test indices with configurable number of folds.

**Algorithm/Method:** K-Fold Cross-Validation (stratified)
**Category:** A (Requires Citation)
**Confidence:** HIGH

**Claim accuracy:** ✅ Accurate
**Citation needed:** Yes
**Suggested citation:** Stone (1978) - Cross-validatory choice and assessment

**Reviewer:** [Your Name]
**Date:** 2025-10-02
```

### Citation Validation Template
```markdown
**Suggested Citation:** Stone (1978)

**Full Reference:**
Stone, M. (1978). Cross-validatory choice and assessment of statistical predictions.
Journal of the Royal Statistical Society: Series B, 36(2), 111-147.
DOI: 10.1080/02331887808801414

**Validation:**
- [ ] ✅ Paper title mentions cross-validation
- [ ] ✅ Abstract describes K-fold methodology
- [ ] ✅ DOI resolves correctly
- [ ] ✅ Seminal work (widely cited)
- [ ] ✅ Peer-reviewed journal (JRSS)

**Code Alignment:**
- [x] Paper describes same algorithm as code
- [x] Topic match: cross-validation → cross-validation
- [x] Appropriate for implementation level

**Approved:** ✅ Yes
**Reviewer:** [Your Name]
```

---

## Category Decision Examples

### Example 1: Super-Twisting Controller

**Code:**
```python
class SuperTwistingController:
    def compute_control(self, state):
        s = self.sliding_surface(state)
        u = -self.k1 * np.sign(s) - self.k2 * np.sign(s) * abs(s)**0.5
        return u
```

**Decision:**
- **Category:** A (REQUIRES CITATION)
- **Rationale:** Implements super-twisting algorithm (mathematical control law)
- **Citation:** Levant (2003) - Higher-order sliding modes

---

### Example 2: Controller Factory Pattern

**Code:**
```python
class ControllerFactory:
    def create_controller(self, controller_type, **kwargs):
        if controller_type == "smc":
            return ClassicalSMC(**kwargs)
        elif controller_type == "sta":
            return SuperTwistingSMC(**kwargs)
        # ... more types
```

**Decision:**
- **Category:** C (NO CITATION NEEDED)
- **Rationale:** Factory design pattern (software implementation)
- **Citation:** None (or optionally "Design Patterns" by Gamma et al.)

---

### Example 3: Reset Method

**Code:**
```python
def reset_state(self):
    """Reset controller internal state to initial values."""
    self.integral_error = 0.0
    self.last_error = 0.0
    self.control_history = []
```

**Decision:**
- **Category:** C (NO CITATION NEEDED)
- **Rationale:** Initialization/reset pattern (pure implementation)
- **Citation:** None

---

### Example 4: K-Fold Cross-Validation

**Code:**
```python
def k_fold_split(self, X, n_splits=5, shuffle=True):
    """Create K-fold cross-validation splits."""
    indices = np.arange(len(X))
    if shuffle:
        np.random.shuffle(indices)
    fold_sizes = np.full(n_splits, len(X) // n_splits, dtype=int)
    # ... split logic
```

**Decision:**
- **Category:** A (REQUIRES CITATION)
- **Rationale:** Implements K-fold cross-validation algorithm
- **Citation:** Stone (1978) - Cross-validatory choice

---

## Lessons Learned from Batch 08

### ❌ Don't Do This

1. **Trust AI Without Verification**
   - ChatGPT cited super-twisting code to genetic algorithms
   - Always read source code yourself

2. **Topic Clustering**
   - All files in `controllers/smc/` → SMC papers
   - Factory patterns in SMC directory still don't need SMC citations

3. **Optimize for Reuse Over Accuracy**
   - Don't group unrelated claims under one citation for convenience
   - Each claim should have the most appropriate citation

4. **Skip Quality Gates**
   - No verification → 41.7% error rate
   - Always run verification before CSV integration

### ✅ Do This

1. **Read Source Code First**
   - Verify claim description matches code
   - Understand what code actually does
   - Categorize before research

2. **Separate Theory from Implementation**
   - Algorithm = needs citation
   - Factory pattern = no citation
   - Reset method = no citation

3. **Use Verification Tools**
   - Automated pattern detection catches obvious errors
   - Sample verification catches subtle issues
   - Peer review ensures quality

4. **Document Decisions**
   - Why this citation?
   - Why no citation?
   - What alternatives were considered?

---

## Batch Completion Checklist

Before marking batch "COMPLETE":

### Triage Phase
- [ ] All claims categorized (A/B/C/D)
- [ ] Category C marked "no citation needed" in CSV
- [ ] Category D manually reviewed and recategorized
- [ ] Triage decisions documented

### Research Phase
- [ ] All Category A/B claims have verified code summaries
- [ ] All citations validated against checklist
- [ ] Citation consistency checked (same method → same citation)
- [ ] All DOIs verified to resolve

### Verification Phase
- [ ] Automated verification script passed
- [ ] Sample verification completed (10% random)
- [ ] Peer review completed (critical claims)
- [ ] Verification report generated and approved

### Integration Phase
- [ ] CSV updated with verified citations
- [ ] Backup CSV created before updates
- [ ] All Research_Status set to "completed"
- [ ] Research_Notes document rationale

### Documentation
- [ ] Batch completion summary created
- [ ] Citation list documented with BibTeX entries
- [ ] Verification report filed in batch directory
- [ ] Lessons learned documented (if applicable)

---

## Success Metrics

### Process Metrics
- **Triage Accuracy:** ≥95% claims correctly categorized
- **Citation Accuracy:** ≥95% citations match code
- **Verification Pass Rate:** ≥90% on first automated check
- **Peer Review Approval:** 100% for critical claims

### Quality Metrics
- **Severe Mismatches:** 0 (control theory for software patterns)
- **Moderate Mismatches:** ≤10% (acceptable for complex domains)
- **Citation Accessibility:** 100% DOIs resolve or URLs provided

### Efficiency Metrics
- **Time per Claim:** ≤15 minutes (including triage + research + verification)
- **Rework Rate:** ≤5% claims require citation revision

---

## Appendix A: Citation Type Guidelines

| Code Type | Citation Type | Example |
|-----------|---------------|---------|
| Mathematical algorithm | Peer-reviewed journal (seminal paper) | Levant (2003) for super-twisting |
| Statistical method | Peer-reviewed journal or book | Stone (1978) for cross-validation |
| Performance metric | Control systems textbook | Ogata (2010) for overshoot |
| Optimization algorithm | Peer-reviewed journal | Clerc & Kennedy (2002) for PSO |
| Software pattern | No citation OR "Design Patterns" book | Factory pattern |
| Initialization code | No citation | Constructor, reset methods |
| Interface definition | No citation | Abstract base class |

---

## Appendix B: Common Pitfalls

**Pitfall 1:** Citing control theory papers for software implementation
- **Example:** Citing Utkin (1977) for `ControllerFactory` class
- **Fix:** No citation needed (factory pattern)

**Pitfall 2:** Citing wrong domain (e.g., MPC for SMC)
- **Example:** Citing Camacho (MPC) for sliding surfaces
- **Fix:** Cite Utkin (SMC)

**Pitfall 3:** Citing general papers for specific methods
- **Example:** Citing generic statistics book for cross-validation
- **Fix:** Cite Stone (1978) specifically for cross-validation

**Pitfall 4:** Not reading the actual paper
- **Example:** Accepting ChatGPT suggestion without verification
- **Fix:** Always verify paper abstract matches code

---

**Workflow Version:** 2.0
**Effective Date:** 2025-10-02
**Replaces:** Implicit workflow from RESEARCH_QUICKSTART.md
**Next Review:** After completing 3 batches with this workflow

**Prepared by:** Claude Code (based on Batch 08 analysis)
**Approved by:** [Pending user approval]
