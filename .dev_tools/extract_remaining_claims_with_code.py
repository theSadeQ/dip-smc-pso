#!/usr/bin/env python3
"""
Extract remaining 108 claims with source code context for ChatGPT prompt
Generates a complete JSON that will be embedded in the markdown prompt
"""
import csv
import json
from pathlib import Path

def read_source_code(file_path, line_num, context_lines=20):
    """Read ±context_lines around line_num from file"""
    try:
        full_path = Path('D:/Projects/main') / file_path.replace('\\', '/')
        if not full_path.exists():
            return f"[FILE NOT FOUND: {file_path}]"

        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)

        code_lines = []
        for i in range(start, end):
            line_marker = ">>>" if i == line_num - 1 else "   "
            code_lines.append(f"{line_marker} {i+1:4d} | {lines[i].rstrip()}")

        return "\n".join(code_lines)
    except Exception as e:
        return f"[ERROR READING FILE: {str(e)}]"

def main():
    # Load claims.json
    claims_json_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json')
    with open(claims_json_path, 'r', encoding='utf-8') as f:
        claims_data = json.load(f)

    claims_by_id = {claim['id']: claim for claim in claims_data['claims']}
    claim_ids_in_json = set(claims_by_id.keys())

    # Load CSV to find uncompleted
    csv_path = Path('D:/Projects/main/artifacts/claims_research_tracker.csv')
    uncompleted_claims = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only process claims that are in claims.json
            if row['Claim_ID'] in claim_ids_in_json and row['Research_Status'] != 'completed':
                claim_info = claims_by_id.get(row['Claim_ID'], {})

                file_path = claim_info.get('file_path', '')
                line_num = int(claim_info.get('line_number', 0)) if claim_info.get('line_number') else 0

                # Read source code only if file path is non-empty
                if file_path and line_num > 0:
                    source_code = read_source_code(file_path, line_num, context_lines=20)
                else:
                    source_code = f"[NO SOURCE FILE - Context only: {claim_info.get('context', 'N/A')}]"

                uncompleted_claims.append({
                    'claim_id': row['Claim_ID'],
                    'file': file_path,
                    'line': line_num,
                    'context': claim_info.get('context', ''),
                    'code': source_code
                })

    # Save to JSON
    output_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/chatgpt_input_108_claims.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(uncompleted_claims, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(uncompleted_claims)} claims with source code")
    print(f"Saved to: {output_path}")

    # Show sample
    if uncompleted_claims:
        print(f"\nSample claim:")
        sample = uncompleted_claims[0]
        print(f"  ID: {sample['claim_id']}")
        print(f"  File: {sample['file']}")
        print(f"  Code preview (first 5 lines):")
        for line in sample['code'].split('\n')[:5]:
            print(f"    {line}")

if __name__ == '__main__':
    main()
