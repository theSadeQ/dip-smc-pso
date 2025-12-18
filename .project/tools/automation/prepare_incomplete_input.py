#!/usr/bin/env python3
#======================================================================================\\\
#===================== .dev_tools/prepare_incomplete_input.py =========================\\\
#======================================================================================\\\

"""
Helper script to prepare incomplete ChatGPT output for citation discovery.

This script helps you save ChatGPT's classification output (ultrathink JSON)
as the incomplete input file for the citation discovery system.

Usage:
    1. Copy ChatGPT's JSON array to clipboard
    2. Run: python .dev_tools/prepare_incomplete_input.py --from-clipboard

    OR

    1. Save ChatGPT's JSON to a temp file
    2. Run: python .dev_tools/prepare_incomplete_input.py --from-file temp.json
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def validate_incomplete_output(data):
    """Validate that the input is incomplete ChatGPT output."""
    errors = []

    if not isinstance(data, list):
        errors.append("Input must be a JSON array")
        return False, errors

    if len(data) != 108:
        errors.append(f"Expected 108 claims, got {len(data)}")

    # Check structure
    for i, claim in enumerate(data[:5]):  # Check first 5
        if 'claim_id' not in claim:
            errors.append(f"Claim {i+1}: Missing 'claim_id'")
        if 'category' not in claim:
            errors.append(f"Claim {i+1}: Missing 'category'")
        if 'code_summary' not in claim:
            errors.append(f"Claim {i+1}: Missing 'code_summary'")

    # Check if it's incomplete (missing citations)
    has_citations = False
    for claim in data[:10]:  # Check first 10
        if claim.get('category') == 'A':
            if claim.get('doi_or_url') or claim.get('paper_title'):
                has_citations = True
                break

    if has_citations:
        errors.append("WARNING: Input appears to have citations already. "
                     "This script is for INCOMPLETE output only.")

    return len(errors) == 0 or errors[0].startswith('WARNING'), errors


def main():
    parser = argparse.ArgumentParser(description="Prepare incomplete ChatGPT output")
    parser.add_argument(
        '--from-file',
        help='Path to file containing ChatGPT JSON'
    )
    parser.add_argument(
        '--from-clipboard',
        action='store_true',
        help='Read JSON from clipboard (requires pyperclip)'
    )
    parser.add_argument(
        '--output',
        default='artifacts/research_batches/08_HIGH_implementation_general/chatgpt_output_108_INCOMPLETE.json',
        help='Where to save the incomplete output'
    )

    args = parser.parse_args()

    print("="*80)
    print("PREPARE INCOMPLETE CHATGPT OUTPUT")
    print("="*80)
    print("")

    # Get JSON data
    if args.from_clipboard:
        print("Reading from clipboard...")
        try:
            import pyperclip
            json_text = pyperclip.paste()
        except ImportError:
            print("ERROR: pyperclip not installed. Install with: pip install pyperclip")
            print("Or use --from-file instead")
            return 1
    elif args.from_file:
        print(f"Reading from file: {args.from_file}")
        try:
            with open(args.from_file, 'r', encoding='utf-8') as f:
                json_text = f.read()
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.from_file}")
            return 1
    else:
        print("ERROR: Must specify --from-clipboard or --from-file")
        print("")
        print("Usage examples:")
        print("  python .dev_tools/prepare_incomplete_input.py --from-clipboard")
        print("  python .dev_tools/prepare_incomplete_input.py --from-file temp.json")
        return 1

    # Parse JSON
    print("Parsing JSON...")
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return 1

    print(f"Loaded {len(data) if isinstance(data, list) else 1} items")
    print("")

    # Validate
    print("Validating structure...")
    is_valid, errors = validate_incomplete_output(data)

    if errors:
        print("Validation issues:")
        for error in errors:
            if error.startswith('WARNING'):
                print(f"  ⚠ {error}")
            else:
                print(f"  ✗ {error}")
        print("")

        if not is_valid:
            print("Cannot proceed with invalid input")
            return 1

    print("✓ Structure validation passed")
    print("")

    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing if present
    if output_path.exists():
        backup_path = output_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        print(f"Backing up existing file to: {backup_path}")
        import shutil
        shutil.copy(output_path, backup_path)

    print(f"Saving to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("")
    print("✓ SUCCESS!")
    print("")
    print("Next steps:")
    print("  1. Run citation discovery:")
    print("     python .dev_tools/citation_discovery_engine.py")
    print("")
    print("  2. Validate output:")
    print("     python .dev_tools/citation_validator.py")
    print("")
    print("  3. Apply citations:")
    print("     python .dev_tools/apply_chatgpt_citations.py")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
