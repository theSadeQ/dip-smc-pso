# Research Quality Checklist Template

**Batch ID:** ____________________
**Researcher:** ____________________
**Date:** ____________________

---

## Phase 0: Triage

### Automated Triage
- [ ] Ran `triage_claims.py` on batch
- [ ] Generated `claims_triaged.json`
- [ ] Reviewed triage report

### Manual Triage Review
- [ ] Verified Category A claims (algorithmic theory)
- [ ] Verified Category C claims (pure implementation)
- [ ] Manually reviewed all Category D claims (uncertain)
- [ ] Spot-checked 10% of automated categorizations

**Category A Count:** ______
**Category B Count:** ______
**Category C Count:** ______ (marked "no citation needed")
**Category D Count:** ______ → ______ (after manual review)

**Gate 1 Status:** [ ] PASS  [ ] FAIL

---

## Phase 1: Code Review

### For Each Category A/B Claim

**Sample Claim Review (Complete for 3 random claims as spot check):**

#### Claim 1: ____________________

- [ ] Read source code (±20 lines context)
- [ ] Verified claim description matches code
- [ ] Identified actual algorithm/method
- [ ] Confirmed citation is needed

**Actual algorithm:** ____________________
**Category correct:** [ ] Yes  [ ] No  → Revised to: ______
**Citation needed:** [ ] Yes  [ ] No

---

#### Claim 2: ____________________

- [ ] Read source code (±20 lines context)
- [ ] Verified claim description matches code
- [ ] Identified actual algorithm/method
- [ ] Confirmed citation is needed

**Actual algorithm:** ____________________
**Category correct:** [ ] Yes  [ ] No  → Revised to: ______
**Citation needed:** [ ] Yes  [ ] No

---

#### Claim 3: ____________________

- [ ] Read source code (±20 lines context)
- [ ] Verified claim description matches code
- [ ] Identified actual algorithm/method
- [ ] Confirmed citation is needed

**Actual algorithm:** ____________________
**Category correct:** [ ] Yes  [ ] No  → Revised to: ______
**Citation needed:** [ ] Yes  [ ] No

---

### Overall Code Review
- [ ] All Category A/B claims have verified summaries
- [ ] Mismatched claim descriptions flagged and corrected
- [ ] Uncertain claims resolved (recategorized)

**Claims requiring code summary corrections:** ______

---

## Phase 2: Citation Research

### ChatGPT Prompts
- [ ] Used verified code summaries in prompts
- [ ] Requested seminal/widely-cited papers
- [ ] Specified peer-reviewed requirement

### Citation Validation

**Sample Citation Validation (Complete for 3 random citations):**

#### Citation 1: ____________________

- [ ] Paper title mentions specific algorithm
- [ ] Abstract describes the method
- [ ] DOI resolves correctly
- [ ] Peer-reviewed journal or top conference
- [ ] Year is reasonable (seminal work)
- [ ] Not a generic review paper

**Topic match:** [ ] Yes  [ ] No
**Approved:** [ ] Yes  [ ] No

---

#### Citation 2: ____________________

- [ ] Paper title mentions specific algorithm
- [ ] Abstract describes the method
- [ ] DOI resolves correctly
- [ ] Peer-reviewed journal or top conference
- [ ] Year is reasonable (seminal work)
- [ ] Not a generic review paper

**Topic match:** [ ] Yes  [ ] No
**Approved:** [ ] Yes  [ ] No

---

#### Citation 3: ____________________

- [ ] Paper title mentions specific algorithm
- [ ] Abstract describes the method
- [ ] DOI resolves correctly
- [ ] Peer-reviewed journal or top conference
- [ ] Year is reasonable (seminal work)
- [ ] Not a generic review paper

**Topic match:** [ ] Yes  [ ] No
**Approved:** [ ] Yes  [ ] No

---

### Citation Consistency
- [ ] Same algorithms cite same sources
- [ ] Citation reuse is logical
- [ ] No topic mismatches (e.g., MPC cited for SMC)

**Unique citations:** ______
**Citation reuse rate:** ______%

**Gate 2 Status:** [ ] PASS  [ ] FAIL

---

## Phase 3: Verification

### Automated Verification
- [ ] Ran `verify_batch_citations.py`
- [ ] Generated verification report
- [ ] Reviewed automated mismatch detection

**Automated verification results:**
- Correct citations: ______ (______%)
- Severe mismatches: ______
- Moderate mismatches: ______
- Uncertain: ______

**Acceptance:** [ ] ≥95% correct  [ ] <95% (requires revision)

---

### Sample Verification (10% Random)

**Random sample size:** ______ claims

**Sampling method:** [ ] Random number generator  [ ] Systematic (every 10th)

**Sample verification results:**

| Claim ID | Citation Correct? | Issues Found |
|----------|-------------------|--------------|
| ________ | [ ] Yes  [ ] No   | ____________ |
| ________ | [ ] Yes  [ ] No   | ____________ |
| ________ | [ ] Yes  [ ] No   | ____________ |
| ________ | [ ] Yes  [ ] No   | ____________ |
| ________ | [ ] Yes  [ ] No   | ____________ |

(Add more rows as needed)

**Pass rate:** ______ / ______ (______%)

**Acceptance:** [ ] ≥95% pass rate  [ ] <95% (requires revision)

---

### Peer Review (Critical Claims)

**Critical claims identified:** ______

**Peer reviewer:** ____________________
**Date:** ____________________

**Critical claims reviewed:**

| Claim ID | Algorithm | Citation | Approved? | Notes |
|----------|-----------|----------|-----------|-------|
| ________ | _________ | ________ | [ ] Yes [ ] No | _____ |
| ________ | _________ | ________ | [ ] Yes [ ] No | _____ |
| ________ | _________ | ________ | [ ] Yes [ ] No | _____ |

**Peer review approval:** [ ] All approved  [ ] Revisions required

**Gate 3 Status:** [ ] PASS  [ ] FAIL

---

## Phase 4: CSV Integration

### Before Integration
- [ ] Created backup of original CSV
- [ ] All corrections documented
- [ ] Verification report approved

### CSV Updates
- [ ] Category C claims marked "no citation needed"
- [ ] Category A/B claims have Suggested_Citation
- [ ] All have BibTeX_Key
- [ ] All have DOI_or_URL (or N/A)
- [ ] All have Reference_Type
- [ ] All have Research_Notes
- [ ] All Research_Status set to "completed"

### After Integration
- [ ] Spot-checked 5 random claims in CSV
- [ ] No formatting errors
- [ ] No missing data

---

## Documentation

- [ ] Batch completion summary created
- [ ] Citation list with BibTeX entries documented
- [ ] Verification report filed in batch directory
- [ ] Lessons learned documented (if applicable)

**Files created:**
- [ ] `BATCH_COMPLETION_SUMMARY.md`
- [ ] `citations.bib` or citation list
- [ ] `verification_report.md`
- [ ] `claims_triaged.json`

---

## Quality Metrics

### Process Metrics
- **Triage accuracy:** ______% (target: ≥95%)
- **Citation accuracy:** ______% (target: ≥95%)
- **Verification pass rate:** ______% (target: ≥90%)
- **Peer review approval:** ______% (target: 100% for critical)

### Quality Metrics
- **Severe mismatches:** ______ (target: 0)
- **Moderate mismatches:** ______% (target: ≤10%)
- **Citation accessibility:** ______% DOIs resolve (target: 100%)

### Efficiency Metrics
- **Time per claim:** ______ minutes (target: ≤15 min)
- **Rework rate:** ______% (target: ≤5%)

---

## Final Approval

### Batch Completion Criteria

- [ ] All quality gates passed (Gates 1, 2, 3)
- [ ] All metrics meet targets
- [ ] Peer review completed and approved
- [ ] Documentation complete
- [ ] CSV updated and verified

**Overall Status:** [ ] COMPLETE  [ ] INCOMPLETE

**Completion notes:**
________________________________________________________________________
________________________________________________________________________
________________________________________________________________________

---

**Researcher Signature:** ____________________
**Date:** ____________________

**Peer Reviewer Signature:** ____________________
**Date:** ____________________

---

## Lessons Learned (Optional)

**What went well:**
________________________________________________________________________
________________________________________________________________________

**What could be improved:**
________________________________________________________________________
________________________________________________________________________

**Process changes recommended:**
________________________________________________________________________
________________________________________________________________________

---

## Appendix: Issue Log

**Issue 1:**
- **Description:** ________________________________________
- **Resolution:** ________________________________________
- **Status:** [ ] Resolved  [ ] Pending

**Issue 2:**
- **Description:** ________________________________________
- **Resolution:** ________________________________________
- **Status:** [ ] Resolved  [ ] Pending

(Add more as needed)

---

**Template Version:** 1.0
**Last Updated:** 2025-10-02
**Compatible With:** RESEARCH_WORKFLOW_V2.md
