# Expected ChatGPT Output - Batch 16_HIGH_sliding_mode_adaptive

**Topic:** Sliding Mode Adaptive
**Claim Count:** 11
**Priority:** HIGH

---

## ⚠️ CITATION QUALITY REQUIREMENTS (READ FIRST!)

### For CRITICAL Priority Batches

**MANDATORY Requirements:**
1. ✅ **Peer-reviewed sources ONLY** (journals or conferences)
2. ❌ **AVOID arXiv preprints** unless no alternative exists
3. ✅ **Prefer authoritative sources:**
   - **Tier 1 (Best):** IEEE Transactions, Automatica, International Journal of Control
   - **Tier 2 (Good):** IEEE Conferences (CDC, ACC, IFAC), Springer journals
   - **Tier 3 (Acceptable):** Seminal textbooks with ISBN/DOI
   - **Tier 4 (Last Resort):** arXiv (ONLY if no Tier 1-3 source exists)

4. ✅ **Verify DOI is valid** - test at https://doi.org/{DOI}
5. ✅ **Check publication year** - prefer sources published BEFORE your implementation (not after)

**Example GOOD Citation (CRITICAL):**
```
- Citation: Clerc & Kennedy (2002)
- BibTeX Key: clerc2002particle
- DOI: 10.1109/4235.985692
- Type: journal
- Note: IEEE Transactions on Evolutionary Computation - foundational PSO stability analysis
```

**Example BAD Citation (CRITICAL):**
```
- Citation: Singh & Padhy (2022)
- BibTeX Key: singh2022modified
- DOI: 10.48550/arXiv.2209.09170  ← arXiv preprint (unpublished)
- Type: arxiv  ← NOT ACCEPTABLE for CRITICAL claims
- Note: Recent work but not peer-reviewed
```

### For HIGH Priority Batches

**Recommended (not mandatory):**
1. ✅ Prefer peer-reviewed sources when available
2. ⚠️ arXiv acceptable if source is authoritative or widely cited
3. ✅ Textbooks and conference papers acceptable
4. ✅ Focus on canonical references (reusable across claims)

---

## Expected Format

After pasting the prompt to ChatGPT, you should receive a response in this EXACT format:

---

**EXAMPLE RESPONSE FROM CHATGPT:**

CLAIM 1 (ID: CODE-IMPL-101):
- Citation: Author (Year)
- BibTeX Key: author_year_keyword
- DOI: 10.XXXX/XXXXX
- Type: journal
- Note: Journal/Conference name - Specific theorem/section/proof covered

CLAIM 2 (ID: CODE-IMPL-119):
- Citation: Author et al. (Year)
- BibTeX Key: author_year_keyword
- DOI: 10.YYYY/YYYYY
- Type: conference
- Note: Conference name - Specific contribution

CLAIM 3 (ID: CODE-IMPL-124):
- Citation: Author (Year)
- BibTeX Key: author_year_keyword  ← Same key as Claim 1 if same source!
- DOI: 10.XXXX/XXXXX
- Type: journal
- Note: Same source as Claim 1. Different section/theorem covered

---

## Validation Checklist

### 1. ✅ **Format Match**
Each claim has exactly 5 fields (Citation, BibTeX Key, DOI, Type, Note)

### 2. ✅ **Citation Format**
"Author (Year)" or "Author1 & Author2 (Year)" or "Author et al. (Year)"

### 3. ✅ **Citation Quality** ⚠️ **CRITICAL FOR HIGH BATCHES**
- **CRITICAL:** All sources MUST be peer-reviewed (no arXiv)
- **HIGH:** Prefer peer-reviewed, arXiv acceptable if canonical
- **Check journal/conference reputation** (IEEE, Springer, Elsevier preferred)

### 4. ✅ **BibTeX Key Consistency** ⚠️ **CRITICAL CHECK**
- **Same source = same BibTeX key** across ALL claims
- Example: If Claims 1 & 3 both cite "Slotine & Li (1991)", both MUST use `slotine1991applied`
- Different chapters of same book = same key (note different chapters in Note field)

### 5. ✅ **DOI Validation**
- Valid DOI format: `10.XXXX/...`
- Test DOI works: https://doi.org/{DOI}
- If book without DOI: acceptable to use "N/A" for textbooks

### 6. ✅ **Type Consistency**
Same source = same type across all claims citing it

### 7. ✅ **Note Quality**
Specific chapter/section/theorem/equation references (NOT generic descriptions)

### 8. ✅ **Citation Reuse Notes**
Claims citing same source should note "Same source as Claim X"

---

## BibTeX Key Consistency Validation

If ChatGPT provides different BibTeX keys for the same source, YOU MUST FIX:

**BEFORE (Inconsistent - WRONG):**
```
CLAIM 1: BibTeX Key: slotine1991applied
CLAIM 3: BibTeX Key: slotine1991boundary  ← ERROR! Same book, different key
```

**AFTER (Consistent - CORRECT):**
```
CLAIM 1: BibTeX Key: slotine1991applied
CLAIM 3: BibTeX Key: slotine1991applied   ← FIXED! Same key
         Note: Same source as Claim 1. Chapter 5 on boundary layer method...
```

**How to Fix:**
1. Identify all claims citing the same book/paper
2. Choose ONE standardized key: `firstauthor_year_keyword` (e.g., `slotine1991applied`)
3. Update ALL claims citing that source to use the same key
4. Add "Same source as Claim X" to Note field for reused citations
5. Note different chapters/sections in the Note field

---

## If Response Needs Corrections

### **If Format is Wrong:**
Ask ChatGPT:
```
Please reformat your response to match the exact structure requested in the original prompt. Each claim needs exactly 5 fields: Citation, BibTeX Key, DOI, Type, and Note.
```

### **If BibTeX Keys Are Inconsistent:**
Ask ChatGPT:
```
For claims citing the same source, please use the same BibTeX key across all instances. For example, if Claims 1 and 3 both cite "Slotine & Li (1991)", both should use the key "slotine1991applied".
```

### **If Citations Are Low Quality (CRITICAL batches):**
Ask ChatGPT:
```
For CLAIM X, you provided an arXiv preprint. For CRITICAL theoretical claims, I need peer-reviewed journal or conference sources. Please suggest 2-3 authoritative alternatives from IEEE Transactions, Automatica, or seminal textbooks, and explain which would be most appropriate.
```

### **If Citations Seem Off:**
Ask for alternatives:
```
For CLAIM X, the suggested citation doesn't seem to match the specific technique described. Can you suggest 2-3 alternative authoritative sources and explain which would be most appropriate?
```

### **If DOI Doesn't Work:**
Verify the DOI:
```
The DOI you provided (10.XXXX/...) doesn't resolve. Can you verify this is correct or provide an alternative DOI or URL for this source?
```

---

## Source Download & Archival

**MANDATORY for all batches:**

After receiving ChatGPT response and verifying quality:

1. **Create sources/ folder** in this batch directory (if not exists)
2. **For EACH unique citation**, download and save:
   - **Journal papers:** Download PDF from DOI link → save as `{bibtex_key}.pdf`
   - **Conference papers:** Download PDF → save as `{bibtex_key}.pdf`
   - **Books:** Save URL or library link → save as `{bibtex_key}_link.txt`
   - **arXiv:** Download PDF → save as `{bibtex_key}_arxiv.pdf`

3. **Save chatgpt_sources.md** in this batch directory

**Example sources/ folder structure:**
```
02_CRITICAL_pso_optimization/
├── sources/
│   ├── clerc2002particle.pdf          # Downloaded from IEEE
│   ├── vandenbergh2006study.pdf       # Downloaded from ScienceDirect
│   ├── erskine2017stochastic.pdf      # Downloaded from Springer
│   ├── shi1998modified.pdf            # Downloaded from IEEE
│   └── README.md                      # List of all sources with URLs
├── chatgpt_sources.md                 # ChatGPT response
├── BATCH_INFO.md
├── INSTRUCTIONS.md
├── PROMPT.md
└── EXPECTED_OUTPUT.md (this file)
```

**Why download sources?**
- **Verification:** Check citation accuracy
- **Archival:** Preserve sources in case of link rot
- **Reference:** Quick access during documentation writing
- **Quality Control:** Ensure sources actually support claims

---

## Expected Citation Reuse

Based on typical research patterns for this topic:
- Many claims may cite the same foundational textbooks or seminal papers
- **Expected reuse rate:** 30-70% (multiple claims per source)
- **Example:** 4 claims might cite only 2 unique sources = 50% reuse rate
- **Benefit:** Faster research! Reuse = efficiency!

---

## Next Steps

### ✅ Response Quality Checklist PASSED:
- [ ] Format verified (5 fields per claim)
- [ ] BibTeX keys consistent (same source = same key)
- [ ] Citation quality meets HIGH requirements
- [ ] DOIs validated (all work or marked N/A)
- [ ] Sources downloaded to sources/ folder
- [ ] chatgpt_sources.md saved

**→ Proceed to INSTRUCTIONS.md Step 4 (Fill CSV)**

### ❌ Response Needs Corrections:
- Format wrong → Ask ChatGPT to reformat
- Keys inconsistent → Fix manually or ask ChatGPT
- Low quality citations → Request peer-reviewed alternatives
- DOI errors → Verify and correct

### ⚠️ Quality Concerns:
- arXiv in CRITICAL batch → MUST replace with peer-reviewed
- Unknown journal/conference → Verify reputation before accepting
- Missing DOI → Try to find DOI via CrossRef or journal website

---

**Generated from template:** `_AUTOMATION/EXPECTED_OUTPUT_TEMPLATE.md`
