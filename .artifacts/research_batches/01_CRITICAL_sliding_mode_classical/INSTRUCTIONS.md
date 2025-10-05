# Step-by-Step Instructions - Batch 01_CRITICAL_sliding_mode_classical

**Topic:** Sliding Mode Classical
**Claims:** 4
**Estimated Time:** ~1.0 hours (60 minutes)
**Per Claim:** ~15 minutes/claim

---

## Prerequisites (Setup - 2 minutes)

**Before starting, you MUST have:**
- [ ] `claims_research_tracker.csv` open in Excel/LibreOffice
- [ ] `PROMPT.md` from this folder open in text editor
- [ ] ChatGPT or Claude open in browser (https://chatgpt.com or https://claude.ai)
- [ ] Notepad/TextEdit open (for backup copies)

**File Locations:**
- CSV: `D:\Projects\main\artifacts\claims_research_tracker.csv`
- Prompt: `D:\Projects\main\artifacts\research_batches\01_CRITICAL_sliding_mode_classical\PROMPT.md`

---

## Step 1: Copy Prompt to ChatGPT (30 seconds)

1. Open `PROMPT.md` in this folder
2. Scroll to "COPY EVERYTHING BELOW THIS LINE"
3. Select ALL text from that line to the end of file
4. Copy (Ctrl+C / Cmd+C)
5. Go to ChatGPT in browser
6. Paste (Ctrl+V / Cmd+V)
7. Press Enter

⏱️ **Time:** 30 seconds

---

## Step 2: Wait for ChatGPT Response (2-5 minutes)

1. ChatGPT will process the request
2. It will generate citations for all 4 claims
3. **IMPORTANT:** As soon as response appears:
   - Select entire response (Ctrl+A)
   - Copy to notepad (Ctrl+C → Ctrl+V)
   - Save as backup: `batch_01_CRITICAL_sliding_mode_classical_response.txt`

**Why backup?** If browser crashes or you lose the response, you don't have to wait again!

⏱️ **Time:** 2-5 minutes (ChatGPT processing)

---

## Step 2.5: Save Response as chatgpt_sources.md (3 minutes)

**IMPORTANT:** Create a permanent record of your research!

1. **Copy template:**
   - Open: `D:\Projects\main\artifacts\research_batches\_AUTOMATION\chatgpt_sources_TEMPLATE.md`
   - Save a copy to this batch folder as `chatgpt_sources.md`

2. **Paste ChatGPT response:**
   - Copy the citation data from ChatGPT
   - Paste into the "Citation Data" section of your new file

3. **Add source documentation:**
   - For each unique source (book/paper), add:
     - Full title and author
     - Accessible URL or DOI
     - Relevant chapters/sections
     - Brief context of what it covers

4. **Verify BibTeX keys:**
   - Check: Same book/paper = same BibTeX key across multiple claims
   - Format: `firstauthor_year_keyword` (e.g., `slotine1991applied`)

5. **Save file:**
   - Location: This batch folder (`01_CRITICAL_sliding_mode_classical/chatgpt_sources.md`)

**Why create this file?**
- Permanent citation record for future reference
- Source documentation for paper writing
- Easy verification and auditing
- Template for remaining batches
- Automated CSV integration (see Step 4.5)

⏱️ **Time:** 3 minutes

---

## Step 3: Verify Output Format (1 minute)

1. Open `EXPECTED_OUTPUT.md` in this folder
2. Compare ChatGPT response to expected format
3. Check each citation has 5 fields:
   - ✅ Citation: Author (Year)
   - ✅ BibTeX Key: author_year_keyword
   - ✅ DOI: 10.XXXX/... or "N/A"
   - ✅ Type: journal/conference/book/arxiv
   - ✅ Note: Specific explanation

**If format is WRONG:**
Ask ChatGPT: *"Please reformat to match the exact structure in the original prompt"*

**If format is CORRECT:**
Proceed to Step 4 ✅

⏱️ **Time:** 1 minute

---

## Step 4: Integrate Citations into CSV (AUTOMATED - 30 seconds)

**NEW: Automated CSV integration!** Instead of manually filling CSV, use the integration script.

### Option A: Automated Integration (Recommended - 30 seconds)

```bash
cd D:\Projects\main
python .dev_tools/claim_extraction/integrate_chatgpt_sources.py \
  --batch "01_CRITICAL_sliding_mode_classical" \
  --verify
```

**What this does:**
- Reads `chatgpt_sources.md` from this folder
- Parses all citation data automatically
- Updates `claims_research_tracker.csv` with 6 tracking columns
- Verifies completion with citation tracker
- Shows citation reuse statistics

**Expected output:**
```
Found 4 claims
Updated 4 claims
2 unique citations -> 4 claims
Citation reuse: 50% efficiency gain!
```

⏱️ **Time:** 30 seconds (vs 10-15 minutes manual!)

---

### Option B: Manual CSV Fill (Fallback - 10 minutes)

**Only use if automation script fails.** For EACH claim in the ChatGPT response, do the following:

### 4a. Find Claim in CSV (30 seconds)

**Method 1 - Filter (Recommended):**
1. Click on `Claim_ID` column header in Excel
2. Click filter icon (▼)
3. Search for: `FORMAL-THEOREM-016`
4. Press Enter → CSV shows only that claim

**Method 2 - Find (Alternative):**
1. Press Ctrl+F (Find)
2. Search for: `FORMAL-THEOREM-016`
3. Click "Find Next" → Jumps to claim row

### 4b. Fill 6 Tracking Columns (2 minutes)

**For the claim row you found, fill these 6 columns:**

| Column # | Column Name | What to Enter | Source in ChatGPT Response |
|----------|-------------|---------------|----------------------------|
| 16 | `Research_Status` | Type: `completed` | (Type manually) |
| 17 | `Suggested_Citation` | Copy citation | Line: "- Citation: Author (Year)" |
| 18 | `BibTeX_Key` | Copy key | Line: "- BibTeX Key: author_year_keyword" |
| 19 | `DOI_or_URL` | Copy DOI | Line: "- DOI: 10.XXXX/..." |
| 20 | `Reference_Type` | Copy type | Line: "- Type: journal/conference/..." |
| 21 | `Research_Notes` | Copy note | Line: "- Note: Explanation..." |

**Example:**

If ChatGPT says:
```
CLAIM 1 (ID: CODE-IMPL-042):
- Citation: Slotine & Li (1991)
- BibTeX Key: slotine1991applied
- DOI: N/A
- Type: book
- Note: Chapter 7, Section 7.3 describes boundary layer method for chattering reduction in sliding mode control
```

You fill:
- Research_Status: `completed`
- Suggested_Citation: `Slotine & Li (1991)`
- BibTeX_Key: `slotine1991applied`
- DOI_or_URL: `N/A`
- Reference_Type: `book`
- Research_Notes: `Chapter 7, Section 7.3 describes boundary layer method for chattering reduction in sliding mode control`

### 4c. Repeat for All Claims

- Claim 1 → Fill 6 columns → Save (Ctrl+S)
- Claim 2 → Fill 6 columns → Save (Ctrl+S)
- ...
- Claim 4 → Fill 6 columns → Save (Ctrl+S)

**💡 Pro Tip:** Save after every 2-3 claims to avoid losing work!

⏱️ **Time per claim:** ~2-3 minutes
⏱️ **Total for 4 claims:** ~10 minutes

---

## Step 5: Verify Completion (2 minutes)

1. **Count filled claims:**
   - In CSV, filter `Claim_ID` column by batch claims
   - Count rows with `Research_Status = "completed"`
   - Should equal: 4 claims

2. **Check all columns filled:**
   - For each completed claim, verify all 6 tracking columns have values
   - No blank cells in columns 16-21

3. **Save final CSV:**
   - Ctrl+S (Save)
   - Close filter if needed

⏱️ **Time:** 2 minutes

---

## Step 6: Track Progress (1 minute)

Run the progress tracker to see your accomplishment:

```bash
cd D:\Projects\main
python .dev_tools/claim_extraction/citation_tracker.py
```

**Expected output:**
- This batch should show **100% complete**
- Overall progress increased
- New citations added to database

⏱️ **Time:** 1 minute

---

## Step 7: Note Reusable Citations (Optional - 1 minute)

**Look for patterns in this batch:**
- Same citation used multiple times?
- Example: "Slotine & Li (1991)" used for 3+ claims
- **Action:** Add to personal citation database for quick lookup in future batches

**How to track:**
Create a simple note file: `my_common_citations.txt`

```
Slotine & Li (1991) - slotine1991applied - Book - Applied Nonlinear Control
  → Use for: boundary layer, classical SMC, Lyapunov stability

Levant (2003) - levant2003higher - Journal - IEEE TAC
  → Use for: super-twisting, higher-order sliding modes, finite-time convergence

Kennedy & Eberhart (1995) - kennedy1995particle - Conference - ICNN
  → Use for: PSO fundamentals, swarm intelligence, optimization
```

**Benefit:** Next batch with same topic → Copy-paste citations → Save 50% time!

⏱️ **Time:** 1 minute (optional, but high ROI!)

---

## Success Criteria ✅

**This batch is COMPLETE when:**
- [ ] All 4 claims have `Research_Status = "completed"`
- [ ] All 4 claims have 6 tracking columns filled (no blanks)
- [ ] ChatGPT response backed up to text file
- [ ] Progress tracker shows batch 100% complete
- [ ] CSV saved successfully

**Time Estimate vs Actual:**
- **Estimated:** 1.0 hours (60 min)
- **Your Actual:** _______ hours _______ minutes (fill in after completion)

---

## Next Batch

After completing this batch, move to next priority batch:
- **Next folder:** `02_01_CRITICAL_sliding_mode/`
- **Location:** `D:\Projects\main\artifacts\research_batches\02_01_CRITICAL_sliding_mode/`

---

## Troubleshooting

### Problem: ChatGPT response is incomplete
**Solution:** Ask ChatGPT: *"Please continue with the remaining claims"*

### Problem: Citations seem generic or irrelevant
**Solution:** Ask ChatGPT: *"For CLAIM X, can you provide more specific citations that directly address [specific technique]?"*

### Problem: Can't find claim in CSV
**Solution:**
1. Check `Claim_ID` is exactly as shown in prompt (case-sensitive)
2. Try Ctrl+F instead of filter
3. Verify CSV file is the correct one (check file date modified)

### Problem: Excel crashed before saving
**Solution:**
1. Reopen CSV
2. Check last saved claim (filter by `Research_Status = "completed"`)
3. Resume from next claim in ChatGPT response (you have backup!)

---

## Questions?

See master workflow guide: `D:\Projects\main\artifacts\RESEARCH_WORKFLOW_GUIDE.md`

---

**Happy researching! 🚀📚**
