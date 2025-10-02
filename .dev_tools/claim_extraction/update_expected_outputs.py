"""
Update EXPECTED_OUTPUT.md Files with Realistic Examples

Generates topic-appropriate example citations showing:
- Real citations (not placeholders)
- Citation reuse patterns (same source = same BibTeX key)
- "Same source as Claim X" notes
- Enhanced quality checks with BibTeX consistency validation
- Expected citation reuse statistics

Usage:
    python update_expected_outputs.py
"""

from pathlib import Path
from typing import Dict, List
import json


# Topic -> Example Citations Mapping (from common_citations.md)
TOPIC_CITATIONS = {
    "sliding_mode_classical": [
        {
            "citation": "Slotine & Li (1991)",
            "key": "slotine1991applied",
            "doi": "N/A",
            "type": "book",
            "note_template": "Chapter {chapter} of *Applied Nonlinear Control* covers {topic}"
        },
        {
            "citation": "Shtessel et al. (2013)",
            "key": "shtessel2013sliding",
            "doi": "10.1007/978-0-8176-4893-0",
            "type": "book",
            "note_template": "Chapter {chapter} of *Sliding Mode Control and Observation* discusses {topic}"
        }
    ],
    "pso_optimization": [
        {
            "citation": "Kennedy & Eberhart (1995)",
            "key": "kennedy1995particle",
            "doi": "10.1109/ICNN.1995.488968",
            "type": "conference",
            "note_template": "Original PSO paper presenting {topic}"
        },
        {
            "citation": "Shi & Eberhart (1998)",
            "key": "shi1998modified",
            "doi": "10.1109/ICEC.1998.699146",
            "type": "conference",
            "note_template": "Introduces {topic} for improved PSO convergence"
        }
    ],
    "control_theory_general": [
        {
            "citation": "Khalil (2002)",
            "key": "khalil2002nonlinear",
            "doi": "N/A",
            "type": "book",
            "note_template": "Chapter {chapter} of *Nonlinear Systems* covers {topic}"
        },
        {
            "citation": "Åström & Wittenmark (2013)",
            "key": "astrom2013adaptive",
            "doi": "N/A",
            "type": "book",
            "note_template": "*Adaptive Control* discusses {topic}"
        }
    ],
    "lyapunov_stability": [
        {
            "citation": "Khalil (2002)",
            "key": "khalil2002nonlinear",
            "doi": "N/A",
            "type": "book",
            "note_template": "Chapter 4 (Lyapunov Stability) covers {topic}"
        },
        {
            "citation": "Slotine & Li (1991)",
            "key": "slotine1991applied",
            "doi": "N/A",
            "type": "book",
            "note_template": "Chapter 3 discusses {topic} with practical examples"
        }
    ],
    "inverted_pendulum": [
        {
            "citation": "Åström & Furuta (2000)",
            "key": "astrom2000swinging",
            "doi": "10.1016/S0005-1098(99)00140-5",
            "type": "journal",
            "note_template": "Energy-based approach to {topic}"
        },
        {
            "citation": "Fantoni & Lozano (2001)",
            "key": "fantoni2001nonlinear",
            "doi": "10.1007/978-1-4471-0177-2",
            "type": "book",
            "note_template": "Underactuated systems theory covering {topic}"
        }
    ],
    "sliding_mode_super_twisting": [
        {
            "citation": "Levant (2003)",
            "key": "levant2003higher",
            "doi": "10.1080/0020717031000099029",
            "type": "journal",
            "note_template": "Original super-twisting algorithm paper covering {topic}"
        },
        {
            "citation": "Moreno & Osorio (2008)",
            "key": "moreno2008lyapunov",
            "doi": "10.1109/CDC.2008.4739356",
            "type": "conference",
            "note_template": "Lyapunov analysis of 2-SMC for {topic}"
        }
    ],
    "fault_detection": [
        {
            "citation": "Ding (2008)",
            "key": "ding2008model",
            "doi": "10.1007/978-1-84882-344-2",
            "type": "book",
            "note_template": "Model-based fault diagnosis covering {topic}"
        },
        {
            "citation": "Chen & Patton (1999)",
            "key": "chen1999robust",
            "doi": "10.1007/978-1-4615-5149-2",
            "type": "book",
            "note_template": "Robust FDI methods for {topic}"
        }
    ],
    "numerical_methods": [
        {
            "citation": "Press et al. (2007)",
            "key": "press2007numerical",
            "doi": "N/A",
            "type": "book",
            "note_template": "*Numerical Recipes* covers {topic}"
        },
        {
            "citation": "Dormand & Prince (1980)",
            "key": "dormand1980family",
            "doi": "10.1016/0771-050X(80)90013-3",
            "type": "journal",
            "note_template": "RK45 method for {topic}"
        }
    ],
    "benchmarking_performance": [
        {
            "citation": "Åström & Murray (2008)",
            "key": "astrom2008feedback",
            "doi": "N/A",
            "type": "book",
            "note_template": "Performance metrics for {topic}"
        },
        {
            "citation": "Franklin et al. (2014)",
            "key": "franklin2014feedback",
            "doi": "N/A",
            "type": "book",
            "note_template": "Control system design covering {topic}"
        }
    ],
    "sliding_mode_adaptive": [
        {
            "citation": "Ioannou & Sun (1996)",
            "key": "ioannou1996robust",
            "doi": "10.1007/978-1-4419-8062-6",
            "type": "book",
            "note_template": "Robust adaptive control for {topic}"
        },
        {
            "citation": "Slotine & Li (1991)",
            "key": "slotine1991applied",
            "doi": "N/A",
            "type": "book",
            "note_template": "Chapters 8-9 cover adaptive control for {topic}"
        }
    ]
}

# Default citations for unmatched topics
DEFAULT_CITATIONS = [
    {
        "citation": "Khalil (2002)",
        "key": "khalil2002nonlinear",
        "doi": "N/A",
        "type": "book",
        "note_template": "Nonlinear systems theory covering {topic}"
    },
    {
        "citation": "Slotine & Li (1991)",
        "key": "slotine1991applied",
        "doi": "N/A",
        "type": "book",
        "note_template": "Applied nonlinear control for {topic}"
    }
]


def generate_realistic_example(topic: str, claim_ids: List[str]) -> str:
    """Generate realistic example citations for a batch."""
    citations = TOPIC_CITATIONS.get(topic, DEFAULT_CITATIONS)
    claim_count = len(claim_ids)

    example = ""
    citation_uses = {}  # Track which citation is used for which claim

    # Pattern: First claim uses citation[0], second uses citation[1],
    # third reuses citation[0] (demonstrates reuse)
    for idx, claim_id in enumerate(claim_ids):
        if idx == 0:
            # First claim - use first citation
            citation_idx = 0
            citation_uses[0] = [1]
        elif idx == 1 and claim_count > 1:
            # Second claim - use second citation
            citation_idx = 1
            citation_uses[1] = [2]
        elif idx >= 2:
            # Third+ claims - reuse earlier citations
            citation_idx = idx % len(citations)
            if citation_idx not in citation_uses:
                citation_uses[citation_idx] = []
            citation_uses[citation_idx].append(idx + 1)
        else:
            citation_idx = 0

        cit = citations[citation_idx]

        # Check if this is a reused citation
        is_reuse = len([c for c in citation_uses.get(citation_idx, []) if c <= idx + 1]) > 1
        first_use_claim = citation_uses[citation_idx][0] if is_reuse else None

        example += f"\nCLAIM {idx + 1} (ID: {claim_id}):\n"
        example += f"- Citation: {cit['citation']}\n"
        example += f"- BibTeX Key: {cit['key']}\n"
        example += f"- DOI: {cit['doi']}\n"
        example += f"- Type: {cit['type']}\n"

        # Generate note
        if is_reuse and first_use_claim:
            example += f"- Note: Same source as Claim {first_use_claim}. "
            example += cit['note_template'].format(
                chapter=idx + 3,
                topic=f"different aspects of the topic (Section {idx}.{idx})"
            )
        else:
            example += f"- Note: {cit['note_template'].format(chapter=idx + 1, topic='the claimed technique')}\n"

        example += "\n"

    return example


def generate_enhanced_checks() -> str:
    """Generate enhanced quality checks section."""
    return """
**What to Check:**

1. ✅ **Format Match:** Each claim has exactly 5 fields (Citation, BibTeX Key, DOI, Type, Note)
2. ✅ **Citation Format:** "Author (Year)" or "Author1 & Author2 (Year)" or "Author et al. (Year)"
3. ✅ **BibTeX Key Consistency:** ⚠️ **CRITICAL CHECK**
   - **Same source = same BibTeX key** across ALL claims
   - Example: If Claims 1 & 3 both cite "Slotine & Li (1991)", both MUST use `slotine1991applied`
   - Different chapters of same book = same key (note different chapters in Note field)
4. ✅ **DOI Format:** Valid DOI (10.XXXX/...) or "N/A" for books without DOI
5. ✅ **Type Consistency:** Same source = same type across all claims citing it
6. ✅ **Note Quality:** Specific chapter/section/theorem/equation references (NOT generic descriptions)
7. ✅ **Citation Reuse Notes:** Claims citing same source should note "Same source as Claim X"

**BibTeX Key Consistency Validation:**

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

**If Format is Wrong:**

Ask ChatGPT:
```
Please reformat your response to match the exact structure requested in the original prompt. Each claim needs exactly 5 fields: Citation, BibTeX Key, DOI, Type, and Note.
```

**If BibTeX Keys Are Inconsistent:**

Ask ChatGPT:
```
For claims citing the same source, please use the same BibTeX key across all instances. For example, if Claims 1 and 3 both cite "Slotine & Li (1991)", both should use the key "slotine1991applied".
```

**If Citations Seem Off:**

Ask for alternatives:
```
For CLAIM X, the suggested citation doesn't seem to match the specific technique described. Can you suggest 2-3 alternative authoritative sources and explain which would be most appropriate?
```

**Expected Citation Reuse:**

Based on typical research patterns for this topic:
- Many claims may cite the same foundational textbooks or seminal papers
- **Expected reuse rate:** 30-70% (multiple claims per source)
- **Example:** 4 claims might cite only 2 unique sources = 50% reuse rate
- **Benefit:** Faster research! Reuse = efficiency!

**Next Steps:**

✅ Response format verified AND BibTeX keys consistent → Save as `chatgpt_sources.md` (Step 2.5)
❌ Format needs fixing → Ask ChatGPT to reformat
⚠️ BibTeX keys inconsistent → Fix keys before proceeding
❓ Uncertain about citations → Ask for alternatives, then proceed

---
"""


def update_expected_output_file(batch_folder: Path, topic: str, claim_count: int):
    """Update EXPECTED_OUTPUT.md for a batch."""
    expected_output_file = batch_folder / "EXPECTED_OUTPUT.md"
    batch_id = batch_folder.name

    # Read claims.json to get real claim IDs
    claims_file = batch_folder / "claims.json"
    if claims_file.exists():
        with open(claims_file, 'r', encoding='utf-8') as f:
            claims_data = json.load(f)
            claim_ids = [c['id'] for c in claims_data.get('claims', [])][:claim_count]
    else:
        # Fallback: generate generic IDs
        claim_ids = [f"CLAIM-ID-{i+1:03d}" for i in range(claim_count)]

    # Generate content
    example = generate_realistic_example(topic, claim_ids)
    enhanced_checks = generate_enhanced_checks()

    # Build complete EXPECTED_OUTPUT.md content
    content = f"""# Expected ChatGPT Output - Batch {batch_id}

**Topic:** {topic.replace('_', ' ').title()}
**Claim Count:** {claim_count}

---

After pasting the prompt to ChatGPT, you should receive a response in this EXACT format:

---

**EXAMPLE RESPONSE FROM CHATGPT:**

{example.strip()}

---

{enhanced_checks}
"""

    # Write file
    with open(expected_output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    """Main execution."""
    base_path = Path(__file__).parent.parent.parent
    batches_path = base_path / "artifacts" / "research_batches"

    print("="*80)
    print("UPDATING EXPECTED_OUTPUT.md FILES")
    print("="*80)
    print()

    # Get all batch folders
    batch_folders = sorted([
        f for f in batches_path.iterdir()
        if f.is_dir() and f.name[0].isdigit()
    ])

    print(f"Found {len(batch_folders)} batch folders\n")

    updated_count = 0
    for batch_folder in batch_folders:
        # Read batch metadata from claims.json
        claims_file = batch_folder / "claims.json"
        if not claims_file.exists():
            print(f"[SKIP] {batch_folder.name} - no claims.json")
            continue

        with open(claims_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        topic = metadata.get('topic', 'unknown')
        claim_count = metadata.get('claim_count', 0)

        # Update EXPECTED_OUTPUT.md
        success = update_expected_output_file(batch_folder, topic, claim_count)

        if success:
            print(f"[OK] {batch_folder.name:<50} ({claim_count} claims, topic: {topic})")
            updated_count += 1
        else:
            print(f"[ERROR] {batch_folder.name}")

    print()
    print("="*80)
    print(f"✅ Updated {updated_count}/{len(batch_folders)} EXPECTED_OUTPUT.md files")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Verify Batch 02 (PSO Optimization) has Kennedy & Eberhart examples")
    print("2. Verify Batch 06 (Super-Twisting) has Levant examples")
    print("3. Spot-check 3-4 other batches for quality")
    print("4. Test workflow with a new batch to verify improvements")
    print()


if __name__ == "__main__":
    main()
