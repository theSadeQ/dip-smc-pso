# ChatGPT Citation Results - Batch [BATCH_ID]

**Topic:** [Topic Name]
**Priority:** [CRITICAL/HIGH/MEDIUM]
**Claim Count:** [N]
**Generated:** [Date]

---

## Citation Data (Copy to CSV using integration script)

CLAIM 1 (ID: [CLAIM-ID-001]):
- Citation: Author (Year)
- BibTeX Key: firstauthor_year_keyword
- DOI: [DOI or URL if book]
- Type: journal/book/conference/arxiv
- Note: [1-2 sentences explaining why this citation fits this specific claim. Include chapter/section/theorem references for books, or equation/figure numbers for papers.]

CLAIM 2 (ID: [CLAIM-ID-002]):
- Citation: Author (Year)
- BibTeX Key: firstauthor_year_keyword
- DOI: [DOI or URL]
- Type: journal/book/conference/arxiv
- Note: [Detailed explanation with specific references]

[... Continue for all claims in batch ...]


---

# Source Documentation

## 1. [First Author] et al. (Year) - *Full Title*

- **Accessible address:** [URL or DOI link]
- **Context:** [Brief description of what this source covers relevant to your claims]
- **Relevant sections:** [Chapters, pages, theorems, equations cited]
- **Key contributions:** [What makes this source authoritative for these claims]
- **Excerpt (optional):** [Verbatim quotes with line/page references if needed]

### Claims using this source:
- CLAIM X (ID: [CLAIM-ID]): [Brief note on which part of source]
- CLAIM Y (ID: [CLAIM-ID]): [Brief note on which part of source]

---

## 2. [Second Source Author] (Year) - *Title*

- **Accessible address:** [URL or DOI]
- **Context:** [What this source covers]
- **Relevant sections:** [Specific chapters/sections]
- **Key contributions:** [Why this source is authoritative]

### Claims using this source:
- CLAIM Z (ID: [CLAIM-ID]): [Note]

---

[... Continue for all unique sources ...]

---

# Integration Checklist

Before running integration script, verify:

- [ ] All claims have 5 citation fields (Citation, BibTeX Key, DOI, Type, Note)
- [ ] BibTeX keys standardized (one key per unique source)
  - [ ] Same book/paper = same BibTeX key across claims
  - [ ] Keys follow format: `firstauthor_year_keyword`
- [ ] Notes include specific chapter/section/theorem/equation references
- [ ] DOIs verified (or URLs provided for books without DOI)
- [ ] All accessible addresses tested (URLs work, DOIs resolve)
- [ ] Source documentation complete for each unique citation

---

# Integration Instructions

**Step 1: Save this file as `chatgpt_sources.md` in your batch folder**
```
artifacts/research_batches/[BATCH_ID]/chatgpt_sources.md
```

**Step 2: Run integration script**
```bash
cd D:\Projects\main
python .dev_tools/claim_extraction/integrate_chatgpt_sources.py \
  --batch "[BATCH_ID]" \
  --verify
```

**Step 3: Verify results**
```bash
python .dev_tools/claim_extraction/citation_tracker.py
```

Expected output:
- Batch [BATCH_ID] shows 100% completion
- Citation reuse rate displayed
- Overall progress updated

---

# Citation Reuse Tracking

**Unique sources in this batch:** [Count]
**Total claims cited:** [Count]
**Reuse efficiency:** [X]%

**Breakdown:**
- [Source 1]: Used for [N] claims
- [Source 2]: Used for [N] claims
- ...

**Pro Tip:** If multiple batches use the same source, add it to `artifacts/common_citations.md` for quick reference in future research!

---

# Quality Assurance

**Citation Quality Checks:**
- [ ] All sources are authoritative (top-tier journals, seminal textbooks, landmark papers)
- [ ] Original sources cited (not just surveys or secondary sources)
- [ ] For theorems: Original proof cited (not just applications)
- [ ] For implementations: Source describing specific technique
- [ ] Publication years verified
- [ ] Author names verified (spelling, et al. usage)

**BibTeX Key Quality:**
- [ ] All keys unique within this batch
- [ ] Keys reusable across batches (consistent naming)
- [ ] Format: `firstauthor_year_keyword` (all lowercase, underscores only)
- [ ] Keywords descriptive (e.g., `slotine1991applied`, not `slotine1991book1`)

---

# Notes for Future Batches

**Common citations found:**
[List any citations that might be reused in other batches]

**Research insights:**
[Any tips for finding citations for this topic]

**Time tracking:**
- Research time: [X] minutes
- Integration time: [Y] minutes
- Total: [Z] minutes
- Estimated: [E] minutes
- Efficiency: [%]

---

**Template Version:** 1.0
**Created:** 2025-10-02
**Last Updated:** [Date when you fill this in]
**Batch Status:** [Not Started / In Progress / Completed]
