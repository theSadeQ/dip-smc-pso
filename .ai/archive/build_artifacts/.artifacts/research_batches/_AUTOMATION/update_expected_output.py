"""
Update EXPECTED_OUTPUT.md files for batches 3-17 with enhanced quality requirements.

Usage:
    python update_expected_output.py
"""

import json
from pathlib import Path

def load_template():
    """Load the EXPECTED_OUTPUT template."""
    template_path = Path(__file__).parent / "EXPECTED_OUTPUT_TEMPLATE.md"
    return template_path.read_text(encoding='utf-8')

def load_batch_plan():
    """Load the research batch plan."""
    plan_path = Path(__file__).parent.parent.parent / "research_batch_plan.json"
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_expected_output(batch_data, template):
    """Generate EXPECTED_OUTPUT.md content for a batch."""

    # Extract batch metadata
    batch_id = batch_data['batch_id']
    topic = batch_data['topic'].replace('_', ' ').title()
    claim_count = batch_data['claim_count']
    priority = batch_data['priority']

    # Get claim IDs for examples
    claim_ids = [claim['id'] for claim in batch_data.get('claims', [])]

    # Fill template placeholders
    content = template.replace('{BATCH_ID}', batch_id)
    content = content.replace('{TOPIC}', topic)
    content = content.replace('{CLAIM_COUNT}', str(claim_count))
    content = content.replace('{PRIORITY}', priority)

    # Add example claim IDs
    if len(claim_ids) >= 1:
        content = content.replace('{CLAIM_ID_1}', claim_ids[0])
    if len(claim_ids) >= 2:
        content = content.replace('{CLAIM_ID_2}', claim_ids[1])
    if len(claim_ids) >= 3:
        content = content.replace('{CLAIM_ID_3}', claim_ids[2])

    # If fewer than 3 claims, use placeholders
    content = content.replace('{CLAIM_ID_1}', 'EXAMPLE-001')
    content = content.replace('{CLAIM_ID_2}', 'EXAMPLE-002')
    content = content.replace('{CLAIM_ID_3}', 'EXAMPLE-003')

    return content

def update_batch_expected_output(batch_folder, batch_data, template):
    """Update EXPECTED_OUTPUT.md for a single batch."""
    output_path = batch_folder / "EXPECTED_OUTPUT.md"

    content = generate_expected_output(batch_data, template)

    output_path.write_text(content, encoding='utf-8')
    print(f"UPDATED: {batch_folder.name}/EXPECTED_OUTPUT.md")

def main():
    """Main execution function."""
    print("Updating EXPECTED_OUTPUT.md files for batches 3-17...")
    print()

    # Load template and batch plan
    template = load_template()
    batch_plan = load_batch_plan()

    # Get research batches directory
    batches_dir = Path(__file__).parent.parent

    # Get all batch folders (sorted)
    batch_folders = sorted([f for f in batches_dir.iterdir() if f.is_dir() and f.name[0].isdigit()])

    # Counters
    updated = 0
    skipped = 0

    # Process all batches (or specific range based on arguments)
    import sys
    if '--all' in sys.argv:
        start_batch = 1
        end_batch = 17
        print("Updating ALL batches (1-17)...")
    else:
        start_batch = 3
        end_batch = 17
        print("Updating batches 3-17...")

    for idx, batch_folder in enumerate(batch_folders):
        batch_num = idx + 1  # Convert to 1-indexed

        # Skip batches outside range
        if batch_num < start_batch or batch_num > end_batch:
            continue

        # Get corresponding batch data from plan
        if idx < len(batch_plan['batches']):
            batch_info = batch_plan['batches'][idx]
        else:
            print(f"WARNING: No batch data for {batch_folder.name}")
            skipped += 1
            continue

        # Create batch data with batch_id and claims from claim_ids
        claims_data = []
        if 'claim_ids' in batch_info:
            for claim_id in batch_info['claim_ids']:
                claims_data.append({'id': claim_id})

        batch_data = {
            'batch_id': batch_folder.name,
            'claims': claims_data,
            **batch_info
        }

        update_batch_expected_output(batch_folder, batch_data, template)
        updated += 1

    print()
    print(f"DONE: Updated {updated} batches")
    if skipped > 0:
        print(f"WARNING: Skipped {skipped} batches")
    print()
    print("All EXPECTED_OUTPUT.md files updated with quality requirements!")
    print()
    print("Next steps:")
    print("1. Review updated files manually")
    print("2. Create sources/ folders in each batch")
    print("3. Update INSTRUCTIONS.md with source download steps")

if __name__ == '__main__':
    main()
