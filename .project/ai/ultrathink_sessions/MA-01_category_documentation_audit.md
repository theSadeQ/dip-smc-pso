# MA-01: Category Documentation Audit

**Type**: Medium Audit
**Duration**: 5 hours
**Scope**: Full documentation category

---

## Session Prompt

```
CATEGORY DOCUMENTATION AUDIT
WHAT: Analyze all documentation in [category] for quality and consistency
WHY:  Ensure category meets documentation standards before publication
HOW:  Aggregate metrics across files, check consistency, verify navigation
WIN:  Category quality report + prioritized improvement roadmap
TIME: 5 hours

TARGET CATEGORY: [INSERT CATEGORY NAME HERE]

INPUTS:
- Category directory: docs/[category]/
- Number of files: [count or "discover"]
- Expected standards: Completeness ≥80%, Accuracy ≥95%, Readability ≥60%

ANALYSIS TASKS:
1. INVENTORY (30 min)
   - List all files in category
   - Calculate total lines
   - Identify file types (.md, .rst, images)
   - Document structure (subdirs, organization)

2. AGGREGATE METRICS (1.5 hours)
   - For each file: completeness %, accuracy %, readability score
   - Calculate category averages
   - Identify outliers (best/worst files)
   - Rank files by quality

3. CONSISTENCY CHECK (1.5 hours)
   - Terminology: same terms for same concepts?
   - Style: consistent heading levels, code formatting?
   - Structure: similar file organization?
   - Cross-references: links work, no dead links?
   - Document inconsistencies

4. NAVIGATION VERIFICATION (1 hour)
   - Check index.md completeness
   - Verify all files linked from index
   - Test breadcrumb trails
   - Verify toctree entries (if Sphinx)
   - Document navigation issues

5. GAP ANALYSIS (30 min)
   - What topics are missing?
   - What files are incomplete?
   - What needs updating?
   - Prioritize gaps by importance

VALIDATION REQUIREMENTS:
1. Manually verify metrics for 5+ random files
2. Click all cross-reference links (verify no 404s)
3. Read 2-3 files end-to-end for coherence

DELIVERABLES:
1. Category quality scorecard (aggregate metrics)
2. File ranking (best to worst)
3. Consistency issues list (with examples)
4. Navigation issues list (broken links, missing entries)
5. Gap analysis (missing topics, incomplete files)
6. Improvement roadmap (prioritized, with effort)

SUCCESS CRITERIA:
- [ ] All files in category analyzed
- [ ] Aggregate metrics calculated
- [ ] 5+ files manually verified
- [ ] All cross-reference links tested
- [ ] Consistency issues documented with examples
- [ ] Improvement roadmap prioritized by impact
- [ ] Can answer: "Is this category ready for users?"
```

---

## Example Usage

```
CATEGORY DOCUMENTATION AUDIT
WHAT: Analyze all documentation in theory/ for quality and consistency
WHY:  Ensure category meets documentation standards before publication
HOW:  Aggregate metrics across files, check consistency, verify navigation
WIN:  Category quality report + prioritized improvement roadmap
TIME: 5 hours

TARGET CATEGORY: theory

INPUTS:
- Category directory: docs/theory/
- Number of files: discover
- Expected standards: Completeness ≥80%, Accuracy ≥95%, Readability ≥60%

[Continue with analysis tasks...]
```

---

## Common Targets

- docs/theory/
- docs/guides/
- docs/architecture/
- docs/testing/
- docs/research/
- docs/deployment/
