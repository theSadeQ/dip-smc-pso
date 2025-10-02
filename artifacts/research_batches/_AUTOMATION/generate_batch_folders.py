"""
Generate Research Batch Folders with Exact Prompts and Workflows

Creates folder structure for each research batch with:
1. PROMPT.md - Exact ChatGPT prompt (copy-paste ready)
2. EXPECTED_OUTPUT.md - What ChatGPT will return
3. INSTRUCTIONS.md - Step-by-step workflow
4. claims.json - Claim details for this batch
5. BATCH_INFO.md - Metadata and progress tracking

Reads from: research_batch_plan.json, claims_inventory.json, claims_research_tracker.csv
Outputs to: artifacts/research_batches/[batch_folders]/
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class BatchFolderGenerator:
    """Generate complete research batch folders with all necessary files."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.artifacts_path = base_path / "artifacts"
        self.batches_path = self.artifacts_path / "research_batches"

        # Load data
        self.batch_plan = self._load_json(self.artifacts_path / "research_batch_plan.json")
        self.claims_inventory = self._load_json(self.artifacts_path / "claims_inventory.json")
        self.csv_claims = self._load_csv(self.artifacts_path / "claims_research_tracker.csv")

        # Citation knowledge base (common references by topic)
        self.citation_kb = {
            "sliding_mode_classical": [
                "Slotine & Li (1991) 'Applied Nonlinear Control'",
                "Utkin (1992) 'Sliding Modes in Control and Optimization'",
                "Edwards & Spurgeon (1998) 'Sliding Mode Control: Theory and Applications'"
            ],
            "super_twisting": [
                "Levant (2003) 'Higher-order sliding modes, differentiation and output-feedback control'",
                "Moreno & Osorio (2008) 'A Lyapunov approach to second-order sliding mode controllers'",
                "Shtessel et al. (2014) 'Sliding Mode Control and Observation' (Chapter 4)"
            ],
            "pso_optimization": [
                "Kennedy & Eberhart (1995) 'Particle swarm optimization'",
                "Shi & Eberhart (1998) 'A modified particle swarm optimizer'",
                "Clerc & Kennedy (2002) 'The particle swarm - explosion, stability, and convergence'"
            ],
            "adaptive_control": [
                "Ioannou & Sun (1996) 'Robust Adaptive Control'",
                "Slotine & Li (1991) 'Applied Nonlinear Control' (Chapters 8-9)",
                "Åström & Wittenmark (2013) 'Adaptive Control' (2nd ed.)"
            ],
            "lyapunov_stability": [
                "Khalil (2002) 'Nonlinear Systems' (3rd ed., Chapter 4)",
                "Slotine & Li (1991) 'Applied Nonlinear Control' (Chapter 3)",
                "Vidyasagar (2002) 'Nonlinear Systems Analysis' (2nd ed.)"
            ],
            "numerical_methods": [
                "Press et al. (2007) 'Numerical Recipes' (3rd ed.)",
                "Dormand & Prince (1980) 'A family of embedded Runge-Kutta formulae'",
                "Shampine & Reichelt (1997) 'The MATLAB ODE Suite'"
            ],
            "inverted_pendulum": [
                "Åström & Furuta (2000) 'Swinging up a pendulum by energy control'",
                "Fantoni & Lozano (2001) 'Non-linear Control for Underactuated Mechanical Systems'",
                "Spong (1995) 'The swing up control problem for the Acrobot'"
            ]
        }

    def _load_json(self, path: Path) -> Dict:
        """Load JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_csv(self, path: Path) -> List[Dict]:
        """Load CSV file as list of dictionaries."""
        with open(path, 'r', encoding='utf-8-sig') as f:
            return list(csv.DictReader(f))

    def get_claims_for_batch(self, batch_info: Dict) -> List[Dict]:
        """Get detailed claim information for a batch."""
        claims_in_batch = []

        # Use claim_ids from batch_info if available
        if 'claim_ids' in batch_info:
            target_ids = batch_info['claim_ids']
            # Match claims from CSV by ID
            for claim in self.csv_claims:
                if claim['Claim_ID'] in target_ids:
                    claims_in_batch.append(claim)
        else:
            # Fallback: Match by priority and topic
            for claim in self.csv_claims:
                if claim['Priority'] == batch_info['priority']:
                    # Simple topic matching
                    if batch_info['topic'].replace('_', ' ') in claim['Research_Description'].lower():
                        claims_in_batch.append(claim)
                        if len(claims_in_batch) >= batch_info['claim_count']:
                            break

        return claims_in_batch[:batch_info['claim_count']]

    def generate_prompt_md(self, batch_info: Dict, claims: List[Dict]) -> str:
        """Generate PROMPT.md content."""
        topic_name = batch_info['topic'].replace('_', ' ').title()
        priority_level = batch_info['priority']

        # Get suggested citations
        suggested_refs = self.citation_kb.get(batch_info['topic'], [
            "[Research relevant authoritative sources for this topic]"
        ])

        prompt = f"""# ChatGPT Research Prompt - Batch {batch_info['batch_id']}

**Topic:** {topic_name}
**Priority:** {priority_level}
**Claim Count:** {len(claims)}

---

**COPY EVERYTHING BELOW THIS LINE AND PASTE TO CHATGPT**

---

I need academic citations for {topic_name.lower()} claims in a control systems research project (Double Inverted Pendulum with Sliding Mode Control and PSO Optimization).

**Context:** These claims describe {topic_name.lower()} implementations and theoretical foundations. I need authoritative citations to support each claim.

**Output Format Required:**
For EACH claim below, provide EXACTLY this format:

```
CLAIM X (ID: [claim_id]):
- Citation: Author (Year)
- BibTeX Key: firstauthor_year_keyword
- DOI: [DOI or "N/A" if book/unavailable]
- Type: journal/conference/book/arxiv
- Note: [1-2 sentences explaining why this citation fits this specific claim]
```

**Claims to Research:**

"""

        # Add each claim
        for idx, claim in enumerate(claims, 1):
            context_text = claim.get('Full_Claim_Text', claim.get('Research_Description', ''))
            if len(context_text) > 200:
                context_text = context_text[:200] + "..."

            prompt += f"""
CLAIM {idx} (ID: {claim['Claim_ID']}):
- Description: "{claim['Research_Description']}"
- Context: "{context_text}"
- File: {claim['File_Path']}
- Line: {claim['Line_Number']}
- Current Status: {claim.get('Existing_Citation_Format', claim.get('Suggested_Citation', 'No citation'))}
- Keywords: {claim['Research_Description'].split()[:5]}

"""

        prompt += f"""

**Suggested Starting References:**
"""
        for ref in suggested_refs:
            prompt += f"- {ref}\n"

        prompt += """

**Important Guidelines:**
1. **Prioritize authoritative sources:**
   - Top-tier journals: IEEE Transactions on Automatic Control, Automatica, Control Engineering Practice
   - Seminal textbooks: Slotine & Li, Khalil, Utkin, etc.
   - Landmark conference papers: CDC, ACC, IFAC

2. **For theorems/lemmas:** Cite the ORIGINAL paper where the theorem was first proven, not surveys or textbooks (unless the textbook is the original source)

3. **For implementations:** Cite the source that best describes the specific technique used (e.g., boundary layer → Slotine & Li Ch. 7)

4. **If uncertain:** Suggest 2-3 alternative citations and note why each might be appropriate

5. **BibTeX keys:** Use format `firstauthor_year_keyword` (e.g., `slotine1991applied`, `levant2003higher`)

---

**AFTER PASTING ABOVE TO CHATGPT:**
1. Wait for response
2. Copy entire response to notepad (backup!)
3. Open EXPECTED_OUTPUT.md to verify format
4. Open INSTRUCTIONS.md for CSV filling steps

---
"""
        return prompt

    def generate_expected_output_md(self, batch_info: Dict, claims: List[Dict]) -> str:
        """Generate EXPECTED_OUTPUT.md content."""
        topic_name = batch_info['topic'].replace('_', ' ').title()

        output = f"""# Expected ChatGPT Output - Batch {batch_info['batch_id']}

**Topic:** {topic_name}
**Claim Count:** {len(claims)}

---

After pasting the prompt to ChatGPT, you should receive a response in this EXACT format:

---

**EXAMPLE RESPONSE FROM CHATGPT:**

"""

        # Generate example outputs for first 2 claims
        examples = min(2, len(claims))
        for idx in range(examples):
            claim = claims[idx]
            output += f"""
CLAIM {idx + 1} (ID: {claim['Claim_ID']}):
- Citation: [Author] (Year)
- BibTeX Key: author_year_keyword
- DOI: [10.XXXX/XXXX or "N/A"]
- Type: [journal/conference/book/arxiv]
- Note: [Explanation of why this citation fits - specific chapter/section reference, theorem number, or technique description]

"""

        if len(claims) > 2:
            output += f"""
[... Citations for remaining {len(claims) - 2} claims in same format ...]

"""

        output += """
---

**What to Check:**

1. ✅ **Format Match:** Each claim has exactly 5 fields (Citation, BibTeX Key, DOI, Type, Note)
2. ✅ **Citation Format:** "Author (Year)" or "Author1 & Author2 (Year)"
3. ✅ **BibTeX Key:** Lowercase, underscores, format `author_year_keyword`
4. ✅ **DOI:** Valid DOI format (10.XXXX/...) or "N/A"
5. ✅ **Type:** One of: journal, conference, book, arxiv
6. ✅ **Note:** Specific explanation (not generic)

**If Format is Wrong:**

Ask ChatGPT:
```
Please reformat your response to match the exact structure requested in the original prompt. Each claim needs exactly 5 fields: Citation, BibTeX Key, DOI, Type, and Note.
```

**If Citations Seem Off:**

Ask for alternatives:
```
For CLAIM X, the suggested citation doesn't seem to match the specific technique described. Can you suggest 2-3 alternative authoritative sources and explain which would be most appropriate?
```

**Next Steps:**

✅ Response format verified → Go to `INSTRUCTIONS.md`
❌ Format needs fixing → Ask ChatGPT to reformat
❓ Uncertain about citations → Ask for alternatives, then proceed

---
"""
        return output

    def generate_instructions_md(self, batch_info: Dict, claims: List[Dict]) -> str:
        """Generate INSTRUCTIONS.md content."""
        topic_name = batch_info['topic'].replace('_', ' ').title()
        claim_count = len(claims)
        time_estimate = batch_info['estimated_time_hours']

        instructions = f"""# Step-by-Step Instructions - Batch {batch_info['batch_id']}

**Topic:** {topic_name}
**Claims:** {claim_count}
**Estimated Time:** ~{time_estimate:.1f} hours ({int(time_estimate * 60)} minutes)
**Per Claim:** ~{int((time_estimate * 60) / claim_count)} minutes/claim

---

## Prerequisites (Setup - 2 minutes)

**Before starting, you MUST have:**
- [ ] `claims_research_tracker.csv` open in Excel/LibreOffice
- [ ] `PROMPT.md` from this folder open in text editor
- [ ] ChatGPT or Claude open in browser (https://chatgpt.com or https://claude.ai)
- [ ] Notepad/TextEdit open (for backup copies)

**File Locations:**
- CSV: `D:\\Projects\\main\\artifacts\\claims_research_tracker.csv`
- Prompt: `D:\\Projects\\main\\artifacts\\research_batches\\{batch_info['batch_id']}\\PROMPT.md`

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
2. It will generate citations for all {claim_count} claims
3. **IMPORTANT:** As soon as response appears:
   - Select entire response (Ctrl+A)
   - Copy to notepad (Ctrl+C → Ctrl+V)
   - Save as backup: `batch_{batch_info['batch_id']}_response.txt`

**Why backup?** If browser crashes or you lose the response, you don't have to wait again!

⏱️ **Time:** 2-5 minutes (ChatGPT processing)

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

## Step 4: Fill CSV for Each Claim ({claim_count} claims × 2-3 min = {int(claim_count * 2.5)} min)

**For EACH claim in the ChatGPT response, do the following:**

### 4a. Find Claim in CSV (30 seconds)

**Method 1 - Filter (Recommended):**
1. Click on `Claim_ID` column header in Excel
2. Click filter icon (▼)
3. Search for: `{claims[0]['Claim_ID'] if claims else 'CLAIM-ID-XXX'}`
4. Press Enter → CSV shows only that claim

**Method 2 - Find (Alternative):**
1. Press Ctrl+F (Find)
2. Search for: `{claims[0]['Claim_ID'] if claims else 'CLAIM-ID-XXX'}`
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
- Claim {claim_count} → Fill 6 columns → Save (Ctrl+S)

**💡 Pro Tip:** Save after every 2-3 claims to avoid losing work!

⏱️ **Time per claim:** ~2-3 minutes
⏱️ **Total for {claim_count} claims:** ~{int(claim_count * 2.5)} minutes

---

## Step 5: Verify Completion (2 minutes)

1. **Count filled claims:**
   - In CSV, filter `Claim_ID` column by batch claims
   - Count rows with `Research_Status = "completed"`
   - Should equal: {claim_count} claims

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
cd D:\\Projects\\main
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
- [ ] All {claim_count} claims have `Research_Status = "completed"`
- [ ] All {claim_count} claims have 6 tracking columns filled (no blanks)
- [ ] ChatGPT response backed up to text file
- [ ] Progress tracker shows batch 100% complete
- [ ] CSV saved successfully

**Time Estimate vs Actual:**
- **Estimated:** {time_estimate:.1f} hours ({int(time_estimate * 60)} min)
- **Your Actual:** _______ hours _______ minutes (fill in after completion)

---

## Next Batch

After completing this batch, move to next priority batch:
- **Next folder:** `{self._get_next_batch_id(batch_info['batch_id'])}/`
- **Location:** `D:\\Projects\\main\\artifacts\\research_batches\\{self._get_next_batch_id(batch_info['batch_id'])}/`

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

See master workflow guide: `D:\\Projects\\main\\artifacts\\RESEARCH_WORKFLOW_GUIDE.md`

---

**Happy researching! 🚀📚**
"""
        return instructions

    def _get_next_batch_id(self, current_batch_id: str) -> str:
        """Get next batch ID based on current."""
        # Simple increment logic
        prefix = current_batch_id.rsplit('_', 1)[0]
        try:
            num = int(current_batch_id.split('_')[0])
            return f"{num + 1:02d}_{prefix}"
        except:
            return "next_batch"

    def generate_claims_json(self, batch_info: Dict, claims: List[Dict]) -> Dict:
        """Generate claims.json content."""
        return {
            "batch_id": batch_info['batch_id'],
            "priority": batch_info['priority'],
            "topic": batch_info['topic'],
            "claim_count": len(claims),
            "estimated_time_hours": batch_info['estimated_time_hours'],
            "generated_date": datetime.now().isoformat(),
            "claims": [
                {
                    "id": claim['Claim_ID'],
                    "description": claim['Research_Description'],
                    "file_path": claim['File_Path'],
                    "line_number": claim['Line_Number'],
                    "context": (claim.get('Full_Claim_Text', claim.get('Research_Description', ''))[:200] + "..."),
                    "current_citation": claim.get('Existing_Citation_Format', claim.get('Suggested_Citation', '')),
                    "keywords": claim['Research_Description'].split()[:5]
                }
                for claim in claims
            ]
        }

    def generate_batch_info_md(self, batch_info: Dict, claims: List[Dict]) -> str:
        """Generate BATCH_INFO.md content."""
        topic_name = batch_info['topic'].replace('_', ' ').title()
        priority = batch_info['priority']
        claim_count = len(claims)
        time_hrs = batch_info['estimated_time_hours']

        # Determine research order
        order_map = {
            "CRITICAL": "1-7 (do FIRST!)",
            "HIGH": "8-20 (do SECOND)",
            "MEDIUM": "21+ (do LAST)"
        }
        research_order = order_map.get(priority, "TBD")

        # Get likely citations
        suggested_refs = self.citation_kb.get(batch_info['topic'], [])

        info = f"""# Batch Information

**Batch ID:** {batch_info['batch_id']}
**Priority:** {priority}
**Topic:** {topic_name}

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Claim Count** | {claim_count} claims |
| **Estimated Time** | ~{time_hrs:.1f} hours ({int(time_hrs * 60)} minutes) |
| **Per Claim** | ~{int((time_hrs * 60) / claim_count)} minutes/claim |
| **Difficulty** | {"High" if priority == "CRITICAL" else "Medium" if priority == "HIGH" else "Low"} |
| **Research Order** | {research_order} |
| **Topic Area** | {topic_name} |

---

## Claims Summary

| # | Claim ID | Type | Description |
|---|----------|------|-------------|
"""

        # Add claim rows
        for idx, claim in enumerate(claims, 1):
            claim_type = "theorem" if "THEOREM" in claim['Claim_ID'] else "lemma" if "LEMMA" in claim['Claim_ID'] else "implementation"
            desc_short = claim['Research_Description'][:60] + "..." if len(claim['Research_Description']) > 60 else claim['Research_Description']
            info += f"| {idx} | {claim['Claim_ID']} | {claim_type} | {desc_short} |\n"

        info += f"""

---

## Likely Citations (Pre-Research Suggestions)

Based on the topic **{topic_name}**, you will likely find references to:

"""

        if suggested_refs:
            for ref in suggested_refs:
                info += f"- {ref}\n"
        else:
            info += "- [Research authoritative sources for this topic]\n"

        info += f"""

**Research Strategy:**
1. Start with these classic references
2. Check if they cover the specific techniques in your claims
3. If not, search for more specific papers (ChatGPT will help!)

---

## Files in This Batch Folder

| File | Purpose |
|------|---------|
| `BATCH_INFO.md` | ← You are here! Overview and metadata |
| `INSTRUCTIONS.md` | Step-by-step workflow (read this next!) |
| `PROMPT.md` | Exact ChatGPT prompt (copy-paste ready) |
| `EXPECTED_OUTPUT.md` | What ChatGPT will return (format verification) |
| `claims.json` | Technical claim data (for automation) |

**Recommended Reading Order:**
1. BATCH_INFO.md (this file) - 2 min
2. INSTRUCTIONS.md - 5 min
3. PROMPT.md - copy to ChatGPT
4. EXPECTED_OUTPUT.md - verify format

---

## Completion Checklist

**Before starting:**
- [ ] Read BATCH_INFO.md (overview)
- [ ] Read INSTRUCTIONS.md (workflow)
- [ ] Open CSV file in Excel
- [ ] Open ChatGPT in browser

**During research:**
- [ ] Prompt copied to ChatGPT
- [ ] Results received and verified against EXPECTED_OUTPUT.md
- [ ] CSV filled ({claim_count} claims × 6 columns = {claim_count * 6} cells)
- [ ] Backup created (ChatGPT response saved to .txt file)

**After completion:**
- [ ] Progress tracker confirms 100% complete
- [ ] All 6 tracking columns filled for each claim
- [ ] CSV saved successfully
- [ ] Reusable citations noted (optional)

---

## Progress Tracking

**Completed Date:** __________ (fill in when done)
**Actual Time:** __________ hours (compare to estimate: {time_hrs:.1f} hours)
**Notes:** __________ (any challenges, insights, or tips for future batches)

---

## Statistics

**Efficiency Metrics (fill in after completion):**
- Time per claim: __________ minutes (target: ~{int((time_hrs * 60) / claim_count)} min/claim)
- Citations found: __________ unique citations
- Reusable citations: __________ (used 2+ times)

**Quality Metrics:**
- All citations authoritative? Yes / No
- All BibTeX keys valid format? Yes / No
- All DOIs checked? Yes / No

---

## Next Steps

After completing this batch:
1. Save CSV (Ctrl+S)
2. Run progress tracker: `python .dev_tools/claim_extraction/citation_tracker.py`
3. Move to next batch folder
4. Celebrate! {claim_count} more claims cited! 🎉

**Next batch:** `{self._get_next_batch_id(batch_info['batch_id'])}/`

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return info

    def create_batch_folder(self, batch_info: Dict, batch_number: int = 1):
        """Create complete batch folder with all 5 files."""
        # Generate batch_id if not present
        if 'batch_id' not in batch_info:
            priority_prefix = batch_info['priority']
            topic = batch_info['topic']
            batch_id = f"{batch_number:02d}_{priority_prefix}_{topic}"
            batch_info['batch_id'] = batch_id
        else:
            batch_id = batch_info['batch_id']

        batch_folder = self.batches_path / batch_id
        batch_folder.mkdir(parents=True, exist_ok=True)

        # Get claims for this batch
        claims = self.get_claims_for_batch(batch_info)

        if not claims:
            print(f"⚠️  No claims found for batch {batch_id}, skipping...")
            return

        # Generate all 5 files
        files_to_create = {
            "PROMPT.md": self.generate_prompt_md(batch_info, claims),
            "EXPECTED_OUTPUT.md": self.generate_expected_output_md(batch_info, claims),
            "INSTRUCTIONS.md": self.generate_instructions_md(batch_info, claims),
            "BATCH_INFO.md": self.generate_batch_info_md(batch_info, claims),
            "claims.json": json.dumps(self.generate_claims_json(batch_info, claims), indent=2)
        }

        # Write files
        for filename, content in files_to_create.items():
            file_path = batch_folder / filename
            file_path.write_text(content, encoding='utf-8')

        print(f"[OK] Created: {batch_id}/ ({len(claims)} claims, {batch_info['estimated_time_hours']:.1f}h)")

    def generate_all_batches(self, priority_filter: str = None):
        """Generate all batch folders (or filtered by priority)."""
        batches = self.batch_plan.get('batches', [])

        if priority_filter:
            batches = [b for b in batches if b['priority'] == priority_filter]

        print(f"\n{'='*80}")
        print(f"GENERATING BATCH FOLDERS")
        print(f"{'='*80}\n")
        print(f"Total batches to create: {len(batches)}")
        if priority_filter:
            print(f"Priority filter: {priority_filter}")
        print()

        for idx, batch in enumerate(batches, 1):
            self.create_batch_folder(batch, batch_number=idx)

        print(f"\n{'='*80}")
        print(f"=== BATCH GENERATION COMPLETE")
        print(f"{'='*80}\n")
        print(f"Created: {len(batches)} batch folders")
        print(f"Location: {self.batches_path}")
        print(f"\nNext steps:")
        print(f"1. Review master index: artifacts/research_batches/_BATCH_INDEX.md")
        print(f"2. Start with first batch: {batches[0]['batch_id'] if batches else 'N/A'}/")
        print()


def main():
    """Main execution."""
    base_path = Path(__file__).parent.parent.parent.parent
    generator = BatchFolderGenerator(base_path)

    # Generate CRITICAL batches first
    print("\n>>> Generating CRITICAL priority batches...")
    generator.generate_all_batches(priority_filter="CRITICAL")

    # Generate HIGH batches (top 10)
    print("\n>>> Generating HIGH priority batches (top 10)...")
    high_batches = [b for b in generator.batch_plan['batches'] if b['priority'] == "HIGH"][:10]
    # Start numbering after CRITICAL batches
    critical_count = len([b for b in generator.batch_plan['batches'] if b['priority'] == "CRITICAL"])
    for idx, batch in enumerate(high_batches, critical_count + 1):
        generator.create_batch_folder(batch, batch_number=idx)

    print("\n=== All batch folders created successfully!")
    print(f"\nTotal folders: {len(list((generator.batches_path).glob('*')))} ")
    print(f"Location: {generator.batches_path}")


if __name__ == "__main__":
    main()
