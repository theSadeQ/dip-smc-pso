"""Quick test script for link validation on sample files."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from validate_docs_links import (
    LinkExtractor, LinkValidator, ValidationResult,
    ReportGenerator, DOCS_ROOT, PROJECT_ROOT
)

def test_sample_files():
    """Test validation on small sample of files."""
    # Test files
    test_files = [
        DOCS_ROOT / "NAVIGATION.md",
        DOCS_ROOT / "index.md",
        DOCS_ROOT / "guides" / "INDEX.md",
        DOCS_ROOT / "api" / "index.md",
    ]

    extractor = LinkExtractor()
    validator = LinkValidator(DOCS_ROOT, PROJECT_ROOT, extractor)
    result = ValidationResult()
    result.total_files = len(test_files)

    print(f"[INFO] Testing {len(test_files)} sample files")

    # Extract and validate
    all_links = []
    for file_path in test_files:
        if not file_path.exists():
            print(f"[WARNING] Skipping {file_path} (not found)")
            continue

        print(f"[INFO] Processing {file_path.name}...")
        links = extractor.extract_links(file_path)
        all_links.extend(links)

        for link in links:
            if link.link_type != 'external':  # Skip external for speed
                issue = validator.validate_link(link)
                if issue:
                    result.add_issue(issue)

    result.total_links = len(all_links)
    result.internal_links = sum(1 for l in all_links if l.link_type != 'external')
    result.external_links = sum(1 for l in all_links if l.link_type == 'external')

    print(f"\n[OK] Extraction complete:")
    print(f"  Total links: {result.total_links}")
    print(f"  Internal: {result.internal_links}")
    print(f"  External: {result.external_links}")
    print(f"  Issues found: {result.critical_errors + result.errors + result.warnings}")

    # Report
    ReportGenerator.console_report(result, verbose=True)

    return result.has_failures()


if __name__ == '__main__':
    failed = test_sample_files()
    sys.exit(1 if failed else 0)
