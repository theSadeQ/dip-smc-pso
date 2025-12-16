#!/usr/bin/env python3
"""
AI Writing Pattern Cleanup Script
Removes AI-generated footers, co-author attribution, and marketing language
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Patterns to remove
AI_FOOTER_PATTERN = r'\n\[AI\] Generated with \[Claude Code\].*?\n+'
CO_AUTHOR_PATTERN = r'\nCo-Authored-By: Claude.*?\n+'
EMOJI_PATTERN = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]'

# Marketing language replacements
MARKETING_REPLACEMENTS = {
    r'\bcomprehensive\b': 'complete',
    r'\bpowerful\b': 'effective',
    r'\brobust\s+controller\b': 'controller with error handling',
    r'\brobust\s+performance\b': 'reliable performance',
    r'\badvanced\s+features\b': 'features',
    r'\bcutting-edge\b': 'current',
}

# Conversational patterns to remove/replace
CONVERSATIONAL_PATTERNS = {
    r"Let's\s+": '',
    r"you'll\s+": 'the system will ',
    r"we'll\s+": 'this will ',
    r"Have you ever\s+": '',
    r"Note that\s+": '',
}

class AIPatternCleaner:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.files_modified = 0
        self.patterns_removed = 0

    def clean_file(self, file_path: Path) -> Tuple[bool, int]:
        """Clean AI patterns from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return False, 0

        original_content = content
        patterns_found = 0

        # Remove AI footers
        content, count = re.subn(AI_FOOTER_PATTERN, '\n', content)
        patterns_found += count

        # Remove co-author attribution
        content, count = re.subn(CO_AUTHOR_PATTERN, '\n', content)
        patterns_found += count

        # Remove emoji (should be none per CLAUDE.md, but check anyway)
        content, count = re.subn(EMOJI_PATTERN, '', content)
        patterns_found += count

        # Replace marketing language
        for pattern, replacement in MARKETING_REPLACEMENTS.items():
            content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            patterns_found += count

        # Remove conversational patterns
        for pattern, replacement in CONVERSATIONAL_PATTERNS.items():
            content, count = re.subn(pattern, replacement, content)
            patterns_found += count

        # Write back if changes were made
        if content != original_content:
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            return True, patterns_found

        return False, 0

    def clean_directory(self, directory: Path, extensions: List[str] = None):
        """Clean all files in a directory"""
        if extensions is None:
            extensions = ['.py', '.md', '.txt', '.rst']

        files_to_clean = []
        for ext in extensions:
            files_to_clean.extend(directory.rglob(f'*{ext}'))

        print(f"[INFO] Found {len(files_to_clean)} files to scan")

        for file_path in files_to_clean:
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '__pycache__', '.pytest_cache']):
                continue

            modified, patterns = self.clean_file(file_path)
            if modified:
                self.files_modified += 1
                self.patterns_removed += patterns
                action = "[DRY RUN]" if self.dry_run else "[CLEANED]"
                print(f"{action} {file_path.relative_to(directory)}: {patterns} patterns")

        print(f"\n[SUMMARY]")
        print(f"  Files modified: {self.files_modified}")
        print(f"  Patterns removed: {self.patterns_removed}")
        if self.dry_run:
            print(f"  [DRY RUN] Use --apply to make changes")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Clean AI writing patterns from codebase')
    parser.add_argument('--directory', default='.', help='Directory to clean')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry run)')
    parser.add_argument('--extensions', nargs='+', default=['.py', '.md'], help='File extensions to process')

    args = parser.parse_args()

    cleaner = AIPatternCleaner(dry_run=not args.apply)
    directory = Path(args.directory).resolve()

    print(f"[INFO] Scanning {directory}")
    print(f"[INFO] Extensions: {args.extensions}")
    print(f"[INFO] Mode: {'DRY RUN' if not args.apply else 'APPLY CHANGES'}")
    print()

    cleaner.clean_directory(directory, args.extensions)

    return 0 if cleaner.files_modified == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
