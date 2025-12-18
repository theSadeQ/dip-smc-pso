"""
Cleanup Test Checkpoint Files
==============================

Removes test and demo checkpoint files while preserving production checkpoints.

Safety Features:
- Dry-run mode by default (use --execute to actually delete)
- Categorizes checkpoints before deletion
- Preserves production work checkpoints
- Logs all actions

Usage:
    python .project/dev_tools/cleanup_test_checkpoints.py              # Dry run
    python .project/dev_tools/cleanup_test_checkpoints.py --execute    # Actually delete
    python .project/dev_tools/cleanup_test_checkpoints.py --all        # Clean ALL checkpoints (risky!)
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def is_test_checkpoint(filename: str, task_id: str) -> bool:
    """
    Determine if a checkpoint is from testing/demo.

    Criteria:
    - Filename contains 'test', 'demo', 'example'
    - Task ID contains 'TEST', 'DEMO', 'EXAMPLE'
    - Filename matches known test patterns
    """
    filename_lower = filename.lower()
    task_lower = task_id.lower()

    test_patterns = [
        'test', 'demo', 'example',
        'token-limit', 'sample', 'tutorial'
    ]

    return any(pattern in filename_lower or pattern in task_lower for pattern in test_patterns)


def get_checkpoint_metadata(checkpoint_file: Path) -> dict:
    """Extract metadata from checkpoint file."""
    try:
        data = json.load(open(checkpoint_file))
        return {
            'task_id': data.get('task_id', 'UNKNOWN'),
            'agent_id': data.get('agent_id', 'UNKNOWN'),
            'status': data.get('status', 'UNKNOWN'),
            'timestamp': data.get('_checkpoint_timestamp', data.get('launched_timestamp', 'UNKNOWN'))
        }
    except Exception as e:
        return {
            'task_id': 'ERROR',
            'agent_id': 'ERROR',
            'status': f'Failed to read: {e}',
            'timestamp': 'UNKNOWN'
        }


def cleanup_test_checkpoints(execute: bool = False, clean_all: bool = False):
    """
    Clean up test checkpoint files.

    Args:
        execute: If True, actually delete files. If False, dry-run mode.
        clean_all: If True, delete ALL checkpoints (dangerous!). If False, only test/demo.
    """
    artifacts = Path('.artifacts')

    if not artifacts.exists():
        print('[ERROR] .artifacts directory not found')
        return

    # Find all checkpoint files
    all_checkpoints = list(artifacts.glob('*_launched.json')) + \
                      list(artifacts.glob('*_progress.json')) + \
                      list(artifacts.glob('*_complete.json')) + \
                      list(artifacts.glob('*_output.json')) + \
                      list(artifacts.glob('*_failed.json')) + \
                      list(artifacts.glob('*_plan_approved.json'))

    if not all_checkpoints:
        print('[OK] No checkpoint files found in .artifacts/')
        return

    # Categorize
    test_checkpoints = []
    production_checkpoints = []

    for checkpoint in all_checkpoints:
        metadata = get_checkpoint_metadata(checkpoint)
        task_id = metadata['task_id']

        if clean_all or is_test_checkpoint(checkpoint.name, task_id):
            test_checkpoints.append((checkpoint, metadata))
        else:
            production_checkpoints.append((checkpoint, metadata))

    # Summary
    mode = '[EXECUTE]' if execute else '[DRY RUN]'
    scope = '[ALL CHECKPOINTS]' if clean_all else '[TEST/DEMO ONLY]'

    print(f'CHECKPOINT CLEANUP {mode} {scope}')
    print('-' * 80)
    print(f'Total checkpoints found: {len(all_checkpoints)}')
    print(f'Test/demo checkpoints: {len(test_checkpoints)}')
    print(f'Production checkpoints: {len(production_checkpoints)}')
    print()

    if not test_checkpoints:
        print('[OK] No test/demo checkpoints to clean up')
        return

    # Show what will be deleted
    print(f'FILES TO DELETE ({len(test_checkpoints)}):')
    print('-' * 80)

    for checkpoint, metadata in sorted(test_checkpoints, key=lambda x: x[1]['task_id']):
        print(f'  {checkpoint.name}')
        print(f'    Task: {metadata["task_id"]}')
        print(f'    Agent: {metadata["agent_id"]}')
        print(f'    Timestamp: {metadata["timestamp"]}')
        print()

    # Show what will be preserved
    if production_checkpoints and not clean_all:
        print(f'FILES TO PRESERVE ({len(production_checkpoints)}):')
        print('-' * 80)
        for checkpoint, metadata in sorted(production_checkpoints, key=lambda x: x[1]['task_id']):
            print(f'  {checkpoint.name} - Task: {metadata["task_id"]}')
        print()

    # Execute deletion if requested
    if execute:
        print('[EXECUTE] Deleting checkpoint files...')
        deleted = 0
        errors = 0

        for checkpoint, metadata in test_checkpoints:
            try:
                checkpoint.unlink()
                deleted += 1
                print(f'[OK] Deleted: {checkpoint.name}')
            except Exception as e:
                errors += 1
                print(f'[ERROR] Failed to delete {checkpoint.name}: {e}')

        print()
        print('-' * 80)
        print(f'SUMMARY:')
        print(f'  Successfully deleted: {deleted}')
        print(f'  Errors: {errors}')
        print(f'  Preserved: {len(production_checkpoints)}')

    else:
        print('[DRY RUN] No files deleted. Use --execute to actually delete.')
        print()
        print('To execute deletion, run:')
        if clean_all:
            print('  python .project/dev_tools/cleanup_test_checkpoints.py --all --execute')
        else:
            print('  python .project/dev_tools/cleanup_test_checkpoints.py --execute')


def main():
    parser = argparse.ArgumentParser(
        description='Clean up test and demo checkpoint files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (show what would be deleted)
  python cleanup_test_checkpoints.py

  # Actually delete test/demo checkpoints
  python cleanup_test_checkpoints.py --execute

  # Delete ALL checkpoints (dangerous!)
  python cleanup_test_checkpoints.py --all --execute
        """
    )
    parser.add_argument('--execute', action='store_true',
                        help='Actually delete files (default: dry run)')
    parser.add_argument('--all', action='store_true',
                        help='Delete ALL checkpoints, not just test/demo (DANGEROUS)')

    args = parser.parse_args()

    if args.all and not args.execute:
        print('[WARNING] --all requires --execute flag for safety')
        print('Add --execute to confirm deletion of ALL checkpoints')
        return

    if args.all:
        confirm = input('DELETE ALL CHECKPOINTS? This will remove production work tracking. Type "yes" to confirm: ')
        if confirm.lower() != 'yes':
            print('[CANCELLED] No files deleted')
            return

    cleanup_test_checkpoints(execute=args.execute, clean_all=args.all)


if __name__ == '__main__':
    main()
