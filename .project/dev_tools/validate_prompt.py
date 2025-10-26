#!/usr/bin/env python3
"""Validate the generated ChatGPT prompt"""
import json
from pathlib import Path

def main():
    prompt_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/CHATGPT_PROMPT_100_PERCENT.md')

    with open(prompt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check sections
    sections = [
        'Project Context',
        'Classification Rules',
        'Input Data: 108 Claims',
        'Your Output Format',
        'Example Outputs',
        'BEGIN PROCESSING'
    ]

    print('Checking prompt structure:')
    all_present = True
    for section in sections:
        if section in content:
            print(f'  [OK] {section}')
        else:
            print(f'  [MISSING] {section}')
            all_present = False

    # Check JSON embedding
    print('')
    if '```json' in content:
        print('[OK] JSON code blocks present')

        # Try to extract and validate the main claims JSON
        json_marker = 'Input Data: 108 Claims'
        if json_marker in content:
            json_start_idx = content.find('```json', content.find(json_marker))
            if json_start_idx != -1:
                json_end_idx = content.find('```', json_start_idx + 7)
                if json_end_idx != -1:
                    json_str = content[json_start_idx+7:json_end_idx].strip()
                    try:
                        claims_data = json.loads(json_str)
                        print(f'[OK] Valid JSON with {len(claims_data)} claims')
                    except json.JSONDecodeError as e:
                        print(f'[ERROR] Invalid JSON: {e}')
    else:
        print('[ERROR] No JSON code blocks found')

    # Stats
    print('')
    print(f'File size: {len(content):,} characters (~{len(content)/1024:.1f} KB)')
    print(f'Estimated words: ~{len(content.split()):,}')
    print(f'Estimated tokens (rough): ~{len(content.split())*1.3:.0f}')

    print('')
    if all_present:
        print('Validation: PASSED')
        print('')
        print('READY TO USE:')
        print(f'1. Open: {prompt_path}')
        print('2. Copy entire file content (Ctrl+A, Ctrl+C)')
        print('3. Paste into ChatGPT')
        print('4. Wait for response (~30-60 minutes)')
        print('5. Save response JSON to chatgpt_output_108_citations.json')
    else:
        print('Validation: FAILED - Missing sections')

if __name__ == '__main__':
    main()
