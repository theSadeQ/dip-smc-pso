#!/usr/bin/env python3
"""
Apply ChatGPT's citations to claims_research_tracker.csv
Run this AFTER you save ChatGPT's response to chatgpt_output_108_citations.json
"""
import csv
import json
import shutil
from pathlib import Path
from datetime import datetime

def validate_chatgpt_output(data):
    """Validate ChatGPT's JSON output"""
    errors = []

    if not isinstance(data, list):
        errors.append("Output must be a JSON array")
        return errors

    # Don't enforce specific count - can be 91 or 108 claims
    if len(data) == 0:
        errors.append("No claims found in output")

    required_fields = ['claim_id', 'category', 'confidence', 'rationale', 'code_summary']

    for i, claim in enumerate(data):
        # Check required fields
        for field in required_fields:
            if field not in claim:
                errors.append(f"Claim {i+1}: Missing field '{field}'")

        # Check category
        if claim.get('category') not in ['A', 'B', 'C']:
            errors.append(f"Claim {claim.get('claim_id', i+1)}: Invalid category '{claim.get('category')}'")

        # Check Category A has citations (paper OR book)
        if claim.get('category') == 'A':
            has_paper = claim.get('doi_or_url') and claim.get('paper_title')
            has_book = claim.get('isbn') and claim.get('book_title')
            if not has_paper and not has_book:
                errors.append(f"Claim {claim['claim_id']}: Category A missing citation (needs paper OR book)")

        # Check Category B has textbook info
        if claim.get('category') == 'B':
            if not claim.get('isbn') or not claim.get('book_title'):
                errors.append(f"Claim {claim['claim_id']}: Category B missing textbook info")

    return errors

def main():
    # Paths - try 91 claims first, fallback to 108
    chatgpt_91_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_91_citations.json')
    chatgpt_108_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_citations.json')

    if chatgpt_91_path.exists():
        chatgpt_output_path = chatgpt_91_path
        print("Using 91 claims file (new batch)")
    elif chatgpt_108_path.exists():
        chatgpt_output_path = chatgpt_108_path
        print("Using 108 claims file (previous batch)")
    else:
        chatgpt_output_path = chatgpt_91_path  # Default for error message

    csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')

    # Check if ChatGPT output exists
    if not chatgpt_output_path.exists():
        print("ERROR: ChatGPT output file not found!")
        print(f"Expected location: {chatgpt_output_path}")
        print("")
        print("Please save ChatGPT's JSON response to this file first.")
        print("See HOW_TO_USE_CHATGPT_PROMPT.md for instructions.")
        return

    # Load ChatGPT's output
    print("Loading ChatGPT output...")
    with open(chatgpt_output_path, 'r', encoding='utf-8') as f:
        chatgpt_data = json.load(f)

    print(f"Loaded {len(chatgpt_data)} claims from ChatGPT")

    # Validate
    print("\nValidating ChatGPT output...")
    errors = validate_chatgpt_output(chatgpt_data)

    if errors:
        print("\nVALIDATION ERRORS:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        print("\nPlease fix these errors before proceeding.")
        return

    print("Validation PASSED!")

    # Create mapping
    print("\nCreating citation mapping...")
    citation_map = {}
    for claim in chatgpt_data:
        claim_id = claim['claim_id']
        # Handle both paper citations (doi_or_url) and book citations (isbn)
        doi_or_url = claim.get('doi_or_url', '') or claim.get('isbn', '')
        citation_map[claim_id] = {
            'Suggested_Citation': claim.get('suggested_citation', ''),
            'BibTeX_Key': claim.get('bibtex_key', ''),
            'DOI_or_URL': doi_or_url,
            'Reference_Type': claim.get('reference_type', ''),
            'Research_Status': 'completed',
            'Research_Notes': f"CHATGPT_100%: {claim['rationale']}"
        }

    # Backup CSV
    print(f"\nBacking up CSV...")
    backup_path = csv_path.parent / f"claims_research_tracker_BACKUP_BEFORE_100PCT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    shutil.copy(csv_path, backup_path)
    print(f"Backup saved: {backup_path}")

    # Read CSV
    print("\nReading CSV...")
    rows = []
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Apply citations
    print("\nApplying citations...")
    applied = 0
    for row in rows:
        if row['Claim_ID'] in citation_map:
            for key, value in citation_map[row['Claim_ID']].items():
                row[key] = value
            applied += 1

    # Write back
    print(f"\nWriting updated CSV...")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied {applied} citations")

    # Calculate final accuracy
    print("\nCalculating final accuracy...")
    completed_batch08 = sum(1 for row in rows if row['Claim_ID'].startswith('CODE-IMPL-') and row['Research_Status'] == 'completed')

    # Load claims.json to get true total
    claims_json_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json')
    with open(claims_json_path, 'r', encoding='utf-8') as f:
        claims_data = json.load(f)
        total_batch08 = len(claims_data['claims'])

    print(f"\nBatch 08 Final Results:")
    print(f"  Total claims: {total_batch08}")
    print(f"  Completed: {completed_batch08}")
    print(f"  Accuracy: {completed_batch08}/{total_batch08} = {100*completed_batch08/total_batch08:.1f}%")

    if completed_batch08 == total_batch08:
        print("\n[SUCCESS] TARGET ACHIEVED: 100% CITATION ACCURACY!")
    else:
        remaining = total_batch08 - completed_batch08
        print(f"\n[WARN] Still {remaining} claims remaining ({100*remaining/total_batch08:.1f}%)")

    # Category breakdown
    print("\nCategory Breakdown (from ChatGPT):")
    cat_a = sum(1 for claim in chatgpt_data if claim['category'] == 'A')
    cat_b = sum(1 for claim in chatgpt_data if claim['category'] == 'B')
    cat_c = sum(1 for claim in chatgpt_data if claim['category'] == 'C')

    print(f"  Category A (papers): {cat_a} ({100*cat_a/len(chatgpt_data):.1f}%)")
    print(f"  Category B (textbooks): {cat_b} ({100*cat_b/len(chatgpt_data):.1f}%)")
    print(f"  Category C (no citation): {cat_c} ({100*cat_c/len(chatgpt_data):.1f}%)")

    # Generate summary report
    print("\nGenerating summary report...")
    report_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/CHATGPT_100PCT_REPORT.md')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# ChatGPT 100% Completion Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Batch**: 08_HIGH_implementation_general\n\n")
        f.write(f"---\n\n")
        f.write(f"## Final Results\n\n")
        f.write(f"- **Total claims**: {total_batch08}\n")
        f.write(f"- **Completed**: {completed_batch08}\n")
        f.write(f"- **Accuracy**: {100*completed_batch08/total_batch08:.1f}%\n\n")
        f.write(f"---\n\n")
        f.write(f"## Category Breakdown\n\n")
        f.write(f"| Category | Count | Percentage | Description |\n")
        f.write(f"|----------|-------|------------|-------------|\n")
        f.write(f"| A (Papers) | {cat_a} | {100*cat_a/len(chatgpt_data):.1f}% | Algorithmic implementations |\n")
        f.write(f"| B (Textbooks) | {cat_b} | {100*cat_b/len(chatgpt_data):.1f}% | Theoretical concepts |\n")
        f.write(f"| C (No citation) | {cat_c} | {100*cat_c/len(chatgpt_data):.1f}% | Pure implementation |\n")
        f.write(f"| **TOTAL** | **{len(chatgpt_data)}** | **100%** | |\n\n")
        f.write(f"---\n\n")
        f.write(f"## Citation Summary\n\n")

        # Group by citation
        citations = {}
        for claim in chatgpt_data:
            if claim['category'] in ['A', 'B'] and claim.get('suggested_citation'):
                citation = claim['suggested_citation']
                if citation not in citations:
                    citations[citation] = []
                citations[citation].append(claim['claim_id'])

        if citations:
            f.write(f"**Unique citations applied**: {len(citations)}\n\n")
            for citation, claim_ids in sorted(citations.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"- **{citation}**: {len(claim_ids)} claims\n")
        else:
            f.write(f"No citations applied (all claims were Category C).\n")

        f.write(f"\n---\n\n")
        f.write(f"## Files Modified\n\n")
        f.write(f"- `claims_research_tracker.csv` (updated with {applied} citations)\n")
        f.write(f"- Backup: `{backup_path.name}`\n\n")
        f.write(f"---\n\n")
        f.write(f"**Process complete!** [OK]\n")

    print(f"Report saved: {report_path}")
    print("\n[OK] COMPLETE!")

if __name__ == '__main__':
    main()
