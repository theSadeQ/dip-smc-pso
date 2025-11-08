"""
Comprehensive Documentation Link Validator

Validates all links in markdown documentation including:
- Markdown links: [text](path.md)
- Sphinx directives: {doc}`path`, {ref}`label`, toctree blocks
- Grid card links: :::{grid-item-card} :link: directive
- Anchor references: [text](#heading)
- External URLs: https://example.com

Features:
- Aggressive auto-fix for common issues
- External URL validation with rate limiting
- Interactive orphan file cleanup
- Parallel processing for performance
- ASCII-only output (Windows cp1252 safe)
- Multiple output formats (console, JSON, markdown)

Usage:
    # Fast mode (internal links only, ~10 seconds)
    python validate_docs_links.py --fast

    # Full mode (all validation except external URLs, ~30 seconds)
    python validate_docs_links.py --full

    # External mode (includes HTTP validation, ~3 minutes)
    python validate_docs_links.py --external

    # Auto-fix mode
    python validate_docs_links.py --fix --dry-run
    python validate_docs_links.py --fix --apply

    # Incremental (changed files only)
    python validate_docs_links.py --incremental

    # JSON export
    python validate_docs_links.py --output results.json
"""

import argparse
import json
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import unquote, urlparse

try:
    from markdown_it import MarkdownIt
    from markdown_it.tree import SyntaxTreeNode
except ImportError:
    print("[ERROR] markdown-it-py not installed. Run: pip install markdown-it-py")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[WARNING] requests not installed. External URL validation disabled.")
    requests = None


# ============================================================================
# Configuration
# ============================================================================

DOCS_ROOT = Path("D:/Projects/main/docs")
PROJECT_ROOT = Path("D:/Projects/main")
CACHE_FILE = PROJECT_ROOT / ".cache" / "link_validation_cache.json"

# Exclusion patterns
EXCLUDE_DIRS = {".git", ".cache", "_build", "venv", "__pycache__", "node_modules"}
EXCLUDE_FILES = {"NAVIGATION.md"}  # Entry points that may appear orphaned

# Link patterns
MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
SPHINX_DOC_PATTERN = re.compile(r'\{doc\}`([^`]+)`')
SPHINX_REF_PATTERN = re.compile(r'\{ref\}`([^`]+)`')
TOCTREE_PATTERN = re.compile(r'```\{toctree\}.*?\n(.*?)```', re.DOTALL)
GRID_CARD_LINK_PATTERN = re.compile(r':::\{grid-item-card\}.*?:link:\s*(\S+)', re.DOTALL)

# External URL validation
MAX_WORKERS_FILES = 8
MAX_WORKERS_URLS = 5
URL_TIMEOUT = 15
URL_RETRIES = 2
URL_RATE_LIMIT = 0.1  # seconds between requests


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Link:
    """Represents a link found in documentation."""
    source_file: Path
    line_number: int
    link_text: str
    link_target: str
    link_type: str  # 'markdown', 'sphinx_doc', 'sphinx_ref', 'toctree', 'grid_card', 'external'
    anchor: Optional[str] = None
    resolved_path: Optional[Path] = None


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str  # 'CRITICAL', 'ERROR', 'WARNING', 'INFO'
    category: str
    file: Path
    line: int
    link_text: str
    link_target: str
    error: str
    auto_fix: Optional[str] = None
    confidence: float = 0.0


@dataclass
class ValidationResult:
    """Results of link validation."""
    total_files: int = 0
    total_links: int = 0
    internal_links: int = 0
    external_links: int = 0
    critical_errors: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    orphaned_files: List[Path] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def add_issue(self, issue: ValidationIssue):
        """Add issue and update counters."""
        self.issues.append(issue)
        if issue.severity == 'CRITICAL':
            self.critical_errors += 1
        elif issue.severity == 'ERROR':
            self.errors += 1
        elif issue.severity == 'WARNING':
            self.warnings += 1
        elif issue.severity == 'INFO':
            self.info += 1

    def has_failures(self) -> bool:
        """Check if there are any failures (strict mode)."""
        return self.critical_errors > 0 or self.errors > 0 or self.warnings > 0

    def duration(self) -> float:
        """Get validation duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


# ============================================================================
# Link Extraction
# ============================================================================

class LinkExtractor:
    """Extracts links from markdown files."""

    def __init__(self, use_markdown_it: bool = True):
        self.use_markdown_it = use_markdown_it
        if use_markdown_it:
            self.md_parser = MarkdownIt()
        self.heading_cache: Dict[Path, List[str]] = {}

    def extract_links(self, file_path: Path) -> List[Link]:
        """Extract all links from a markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[WARNING] Could not read {file_path}: {e}")
            return []

        links = []
        lines = content.split('\n')

        # Extract markdown links
        for i, line in enumerate(lines, 1):
            # Markdown links: [text](target)
            for match in MARKDOWN_LINK_PATTERN.finditer(line):
                text, target = match.groups()
                link_type = 'external' if self._is_external(target) else 'markdown'
                anchor = None
                if '#' in target:
                    target, anchor = target.split('#', 1)

                links.append(Link(
                    source_file=file_path,
                    line_number=i,
                    link_text=text,
                    link_target=target,
                    link_type=link_type,
                    anchor=anchor
                ))

            # Sphinx doc roles: {doc}`path`
            for match in SPHINX_DOC_PATTERN.finditer(line):
                target = match.group(1)
                links.append(Link(
                    source_file=file_path,
                    line_number=i,
                    link_text=target,
                    link_target=target,
                    link_type='sphinx_doc'
                ))

            # Sphinx ref roles: {ref}`label`
            for match in SPHINX_REF_PATTERN.finditer(line):
                target = match.group(1)
                links.append(Link(
                    source_file=file_path,
                    line_number=i,
                    link_text=target,
                    link_target=target,
                    link_type='sphinx_ref'
                ))

        # Extract toctree entries
        for match in TOCTREE_PATTERN.finditer(content):
            toctree_content = match.group(1)
            for line_num, line in enumerate(toctree_content.split('\n'), 1):
                line = line.strip()
                if line and not line.startswith(':'):
                    # Handle glob patterns
                    if '*' in line:
                        links.append(Link(
                            source_file=file_path,
                            line_number=line_num,
                            link_text=line,
                            link_target=line,
                            link_type='toctree_glob'
                        ))
                    else:
                        links.append(Link(
                            source_file=file_path,
                            line_number=line_num,
                            link_text=line,
                            link_target=line,
                            link_type='toctree'
                        ))

        # Extract grid card links
        for match in GRID_CARD_LINK_PATTERN.finditer(content):
            target = match.group(1)
            links.append(Link(
                source_file=file_path,
                line_number=1,  # Hard to get exact line from regex
                link_text=target,
                link_target=target,
                link_type='grid_card'
            ))

        return links

    def extract_headings(self, file_path: Path) -> List[str]:
        """Extract all headings from a markdown file."""
        if file_path in self.heading_cache:
            return self.heading_cache[file_path]

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        headings = []
        for line in content.split('\n'):
            if line.strip().startswith('#'):
                # Extract heading text (remove # markers)
                heading_text = re.sub(r'^#+\s*', '', line).strip()
                headings.append(heading_text)

        self.heading_cache[file_path] = headings
        return headings

    @staticmethod
    def _is_external(target: str) -> bool:
        """Check if link target is external URL."""
        return target.startswith(('http://', 'https://', 'ftp://', 'mailto:'))

    @staticmethod
    def heading_to_anchor(heading: str) -> str:
        """Convert heading text to Sphinx anchor ID."""
        # Sphinx anchor generation rules:
        # 1. Lowercase
        # 2. Replace spaces with hyphens
        # 3. Remove special characters except hyphens
        # 4. Strip code backticks
        anchor = heading.lower()
        anchor = re.sub(r'`([^`]+)`', r'\1', anchor)  # Remove backticks
        anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove special chars
        anchor = re.sub(r'[\s]+', '-', anchor)  # Spaces to hyphens
        anchor = re.sub(r'-+', '-', anchor)  # Collapse multiple hyphens
        anchor = anchor.strip('-')  # Strip leading/trailing hyphens
        return anchor


# ============================================================================
# Link Validator
# ============================================================================

class LinkValidator:
    """Validates links in documentation."""

    def __init__(self, docs_root: Path, project_root: Path, extractor: LinkExtractor):
        self.docs_root = docs_root
        self.project_root = project_root
        self.extractor = extractor
        self.file_cache: Set[Path] = set()
        self._populate_file_cache()

    def _populate_file_cache(self):
        """Populate cache of all markdown files."""
        for ext in ['*.md', '*.MD']:
            self.file_cache.update(self.docs_root.rglob(ext))
            self.file_cache.update((self.project_root / ".project").rglob(ext))

    def validate_link(self, link: Link) -> Optional[ValidationIssue]:
        """Validate a single link."""
        if link.link_type == 'external':
            # External URLs validated separately
            return None

        if link.link_type == 'sphinx_ref':
            # Sphinx references require parsing label definitions (complex)
            # Skip for now, delegate to Sphinx linkcheck
            return None

        if link.link_type == 'toctree_glob':
            # Glob patterns require expansion
            return self._validate_glob_pattern(link)

        # Validate file existence
        resolved_path = self._resolve_path(link)
        if not resolved_path:
            return ValidationIssue(
                severity='CRITICAL',
                category='broken_internal_link',
                file=link.source_file,
                line=link.line_number,
                link_text=link.link_text,
                link_target=link.link_target,
                error='File not found',
                auto_fix=self._suggest_file_fix(link),
                confidence=0.8
            )

        link.resolved_path = resolved_path

        # Validate anchor if present
        if link.anchor:
            anchor_issue = self._validate_anchor(link, resolved_path)
            if anchor_issue:
                return anchor_issue

        return None

    def _resolve_path(self, link: Link) -> Optional[Path]:
        """Resolve link target to absolute path."""
        target = link.link_target

        # Handle empty or anchor-only links
        if not target or target.startswith('#'):
            return link.source_file

        # Handle Sphinx doc/toctree refs (no extension)
        if link.link_type in ('sphinx_doc', 'toctree', 'grid_card'):
            # Try with .md extension
            if not target.endswith('.md'):
                target_md = target + '.md'
            else:
                target_md = target

            # Resolve relative to docs root
            if link.source_file.is_relative_to(self.docs_root):
                base_dir = link.source_file.parent
            else:
                base_dir = self.docs_root

            resolved = (base_dir / target_md).resolve()
            if resolved.exists():
                return resolved

            # Try without extension (Sphinx may use .rst)
            resolved_no_ext = (base_dir / target).resolve()
            if resolved_no_ext.exists():
                return resolved_no_ext

            # Try relative to docs root
            resolved_root = (self.docs_root / target_md).resolve()
            if resolved_root.exists():
                return resolved_root

            return None

        # Handle markdown links with .html extension (build artifacts)
        if target.endswith('.html'):
            target = target[:-5] + '.md'

        # Resolve relative path
        base_dir = link.source_file.parent
        resolved = (base_dir / target).resolve()

        if resolved.exists():
            return resolved

        # Try case-insensitive match (Windows)
        for cached_file in self.file_cache:
            if cached_file.resolve() == resolved:
                return cached_file
            if str(cached_file.resolve()).lower() == str(resolved).lower():
                return cached_file

        return None

    def _validate_anchor(self, link: Link, target_file: Path) -> Optional[ValidationIssue]:
        """Validate anchor exists in target file."""
        headings = self.extractor.extract_headings(target_file)
        anchor_ids = [self.extractor.heading_to_anchor(h) for h in headings]

        if link.anchor not in anchor_ids:
            # Try URL-decoded version
            decoded_anchor = unquote(link.anchor)
            if decoded_anchor not in anchor_ids:
                return ValidationIssue(
                    severity='ERROR',
                    category='invalid_anchor',
                    file=link.source_file,
                    line=link.line_number,
                    link_text=link.link_text,
                    link_target=f"{link.link_target}#{link.anchor}",
                    error=f"Anchor not found (available: {', '.join(anchor_ids[:5])}...)",
                    auto_fix=self._suggest_anchor_fix(link, anchor_ids),
                    confidence=0.7
                )

        return None

    def _validate_glob_pattern(self, link: Link) -> Optional[ValidationIssue]:
        """Validate glob pattern in toctree."""
        pattern = link.link_target
        base_dir = link.source_file.parent

        try:
            matches = list(base_dir.glob(pattern + '.md'))
            if not matches:
                return ValidationIssue(
                    severity='WARNING',
                    category='empty_glob',
                    file=link.source_file,
                    line=link.line_number,
                    link_text=link.link_text,
                    link_target=pattern,
                    error='Glob pattern matches no files',
                    confidence=0.5
                )
        except Exception as e:
            return ValidationIssue(
                severity='ERROR',
                category='invalid_glob',
                file=link.source_file,
                line=link.line_number,
                link_text=link.link_text,
                link_target=pattern,
                error=f'Invalid glob pattern: {e}',
                confidence=0.0
            )

        return None

    def _suggest_file_fix(self, link: Link) -> Optional[str]:
        """Suggest auto-fix for missing file."""
        target = link.link_target

        # Check if .html version exists
        if target.endswith('.md'):
            html_version = target[:-3] + '.html'
            if self._resolve_path(Link(link.source_file, link.line_number, '', html_version, 'markdown')):
                return target  # Already correct

        # Check if .md version exists (target was .html)
        if target.endswith('.html'):
            md_version = target[:-5] + '.md'
            if self._resolve_path(Link(link.source_file, link.line_number, '', md_version, 'markdown')):
                return md_version

        # Check case sensitivity
        resolved = self._case_insensitive_match(link)
        if resolved:
            return str(resolved.relative_to(link.source_file.parent))

        # Check if file was moved (git history)
        moved_path = self._find_moved_file(link)
        if moved_path:
            return str(moved_path.relative_to(link.source_file.parent))

        return None

    def _suggest_anchor_fix(self, link: Link, available_anchors: List[str]) -> Optional[str]:
        """Suggest auto-fix for invalid anchor."""
        # Find closest match (simple similarity)
        target_anchor = link.anchor.lower()
        best_match = None
        best_score = 0

        for anchor in available_anchors:
            score = self._similarity(target_anchor, anchor)
            if score > best_score and score > 0.6:
                best_score = score
                best_match = anchor

        if best_match:
            return f"{link.link_target}#{best_match}"

        return None

    def _case_insensitive_match(self, link: Link) -> Optional[Path]:
        """Find case-insensitive match for file."""
        target = link.link_target
        base_dir = link.source_file.parent
        resolved = (base_dir / target).resolve()

        for cached_file in self.file_cache:
            if str(cached_file.resolve()).lower() == str(resolved).lower():
                return cached_file

        return None

    def _find_moved_file(self, link: Link) -> Optional[Path]:
        """Find moved file via git history."""
        # This would require git log parsing - complex
        # For now, return None (can implement later)
        return None

    @staticmethod
    def _similarity(s1: str, s2: str) -> float:
        """Calculate simple string similarity (0-1)."""
        if not s1 or not s2:
            return 0.0

        # Jaccard similarity on character bigrams
        bigrams1 = {s1[i:i+2] for i in range(len(s1)-1)}
        bigrams2 = {s2[i:i+2] for i in range(len(s2)-1)}

        if not bigrams1 or not bigrams2:
            return 0.0

        intersection = bigrams1 & bigrams2
        union = bigrams1 | bigrams2

        return len(intersection) / len(union)


# ============================================================================
# External URL Validator
# ============================================================================

class ExternalURLValidator:
    """Validates external HTTP/HTTPS links."""

    def __init__(self, timeout: int = URL_TIMEOUT, retries: int = URL_RETRIES):
        self.timeout = timeout
        self.retries = retries
        self.session = None
        if requests:
            self.session = requests.Session()
            self.session.headers.update({'User-Agent': 'Documentation-Link-Validator/1.0'})

    def validate_url(self, link: Link) -> Optional[ValidationIssue]:
        """Validate external URL."""
        if not self.session:
            return ValidationIssue(
                severity='INFO',
                category='url_validation_skipped',
                file=link.source_file,
                line=link.line_number,
                link_text=link.link_text,
                link_target=link.link_target,
                error='requests library not installed',
                confidence=0.0
            )

        url = link.link_target

        # Skip localhost and local network
        parsed = urlparse(url)
        if parsed.hostname in ('localhost', '127.0.0.1') or (parsed.hostname and parsed.hostname.endswith('.local')):
            return None

        # Try HEAD request first (faster)
        for attempt in range(self.retries + 1):
            try:
                response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
                if response.status_code < 400:
                    return None  # Success

                # Try GET if HEAD failed
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
                if response.status_code < 400:
                    return None  # Success

                # URL is broken
                return ValidationIssue(
                    severity='WARNING',
                    category='broken_external_url',
                    file=link.source_file,
                    line=link.line_number,
                    link_text=link.link_text,
                    link_target=url,
                    error=f'HTTP {response.status_code}',
                    confidence=0.9
                )

            except requests.exceptions.Timeout:
                if attempt < self.retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return ValidationIssue(
                    severity='WARNING',
                    category='url_timeout',
                    file=link.source_file,
                    line=link.line_number,
                    link_text=link.link_text,
                    link_target=url,
                    error=f'Timeout after {self.timeout}s',
                    confidence=0.5
                )

            except requests.exceptions.RequestException as e:
                return ValidationIssue(
                    severity='WARNING',
                    category='url_connection_error',
                    file=link.source_file,
                    line=link.line_number,
                    link_text=link.link_text,
                    link_target=url,
                    error=str(e)[:100],
                    confidence=0.7
                )

        return None


# ============================================================================
# Auto-Fix Engine
# ============================================================================

class AutoFixer:
    """Automatically fix common link issues."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.fixes_failed = 0

    def apply_fixes(self, issues: List[ValidationIssue]) -> Dict[Path, List[str]]:
        """Apply auto-fixes to issues."""
        fixes_by_file: Dict[Path, List[Tuple[int, str, str]]] = {}

        # Group fixes by file
        for issue in issues:
            if issue.auto_fix and issue.confidence > 0.5:  # Apply all fixes > 50% confidence
                if issue.file not in fixes_by_file:
                    fixes_by_file[issue.file] = []

                fixes_by_file[issue.file].append((
                    issue.line,
                    issue.link_target,
                    issue.auto_fix
                ))

        # Apply fixes file by file
        results = {}
        for file_path, fixes in fixes_by_file.items():
            result = self._apply_file_fixes(file_path, fixes)
            results[file_path] = result

        return results

    def _apply_file_fixes(self, file_path: Path, fixes: List[Tuple[int, str, str]]) -> List[str]:
        """Apply fixes to a single file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.fixes_failed += 1
            return [f"[ERROR] Could not read file: {e}"]

        # Create backup
        if not self.dry_run:
            backup_path = file_path.with_suffix(f'.md.backup.{int(time.time())}')
            shutil.copy2(file_path, backup_path)

        lines = content.split('\n')
        applied_fixes = []

        # Apply fixes (sorted by line number descending to preserve line numbers)
        for line_num, old_target, new_target in sorted(fixes, reverse=True):
            if 0 < line_num <= len(lines):
                old_line = lines[line_num - 1]
                new_line = old_line.replace(old_target, new_target)

                if old_line != new_line:
                    lines[line_num - 1] = new_line
                    applied_fixes.append(f"Line {line_num}: {old_target} -> {new_target}")
                    self.fixes_applied += 1

        # Write back
        if applied_fixes and not self.dry_run:
            try:
                file_path.write_text('\n'.join(lines), encoding='utf-8')
            except Exception as e:
                self.fixes_failed += 1
                return [f"[ERROR] Could not write file: {e}"]

        return applied_fixes


# ============================================================================
# Orphan Detector
# ============================================================================

class OrphanDetector:
    """Detects orphaned files not linked from anywhere."""

    def __init__(self, docs_root: Path, exclude_files: Set[str]):
        self.docs_root = docs_root
        self.exclude_files = exclude_files
        self.link_graph: Dict[Path, Set[Path]] = {}

    def build_link_graph(self, all_links: List[Link]):
        """Build graph of file dependencies."""
        for link in all_links:
            if link.link_type != 'external' and link.resolved_path:
                if link.resolved_path not in self.link_graph:
                    self.link_graph[link.resolved_path] = set()
                self.link_graph[link.resolved_path].add(link.source_file)

    def find_orphans(self, all_files: List[Path]) -> List[Path]:
        """Find files with no incoming links."""
        orphans = []

        for file_path in all_files:
            # Skip excluded files
            if file_path.name in self.exclude_files:
                continue

            # Skip index files (may be linked via toctree)
            if file_path.name.lower() == 'index.md':
                continue

            # Skip archived files
            if '.project/archive' in str(file_path):
                continue

            # Check if file has incoming links
            if file_path not in self.link_graph or not self.link_graph[file_path]:
                orphans.append(file_path)

        return orphans

    def interactive_cleanup(self, orphans: List[Path], dry_run: bool = True) -> Dict[str, int]:
        """Interactive cleanup of orphaned files."""
        stats = {'moved': 0, 'deleted': 0, 'kept': 0, 'errors': 0}

        if dry_run:
            print(f"\n[INFO] Dry-run mode: showing {len(orphans)} orphaned files")
            for orphan in orphans:
                print(f"  - {orphan.relative_to(PROJECT_ROOT)}")
            return stats

        print(f"\n[INFO] Found {len(orphans)} orphaned files")
        print("[INFO] Options: (m)ove to archive, (d)elete, (k)eep, (a)bort")

        archive_dir = PROJECT_ROOT / ".project" / "archive" / "orphaned_docs"
        archive_dir.mkdir(parents=True, exist_ok=True)

        for orphan in orphans:
            rel_path = orphan.relative_to(PROJECT_ROOT)
            print(f"\n{rel_path}")
            print(f"  Last modified: {datetime.fromtimestamp(orphan.stat().st_mtime)}")

            choice = input("  Action [m/d/k/a]? ").strip().lower()

            if choice == 'a':
                print("[INFO] Cleanup aborted")
                break
            elif choice == 'm':
                try:
                    dest = archive_dir / orphan.name
                    shutil.move(str(orphan), str(dest))
                    print(f"  [OK] Moved to {dest.relative_to(PROJECT_ROOT)}")
                    stats['moved'] += 1
                except Exception as e:
                    print(f"  [ERROR] Failed to move: {e}")
                    stats['errors'] += 1
            elif choice == 'd':
                confirm = input("  Confirm deletion [y/N]? ").strip().lower()
                if confirm == 'y':
                    try:
                        orphan.unlink()
                        print("  [OK] Deleted")
                        stats['deleted'] += 1
                    except Exception as e:
                        print(f"  [ERROR] Failed to delete: {e}")
                        stats['errors'] += 1
                else:
                    print("  [INFO] Skipped")
                    stats['kept'] += 1
            else:
                print("  [INFO] Kept")
                stats['kept'] += 1

        return stats


# ============================================================================
# Report Generator
# ============================================================================

class ReportGenerator:
    """Generates validation reports in multiple formats."""

    @staticmethod
    def console_report(result: ValidationResult, verbose: bool = False):
        """Generate ASCII console report (Windows-safe)."""
        print("\n" + "=" * 80)
        print("[INFO] Link Validation Report")
        print("=" * 80)
        print(f"Documentation: {DOCS_ROOT} ({result.total_files} files)")
        print(f"Links Checked: {result.total_links} ({result.internal_links} internal, {result.external_links} external)")
        print(f"Duration: {result.duration():.1f}s")
        print()

        # Summary
        if result.critical_errors > 0:
            print(f"[CRITICAL] {result.critical_errors} broken internal links")
        if result.errors > 0:
            print(f"[ERROR] {result.errors} validation errors")
        if result.warnings > 0:
            print(f"[WARNING] {result.warnings} warnings")
        if result.info > 0:
            print(f"[INFO] {result.info} informational messages")

        if result.orphaned_files:
            print(f"[INFO] {len(result.orphaned_files)} orphaned files")

        # Detailed issues
        if verbose and result.issues:
            print("\n" + "-" * 80)
            print("Detailed Issues:")
            print("-" * 80)

            for issue in sorted(result.issues, key=lambda x: (x.severity, str(x.file))):
                print(f"\n[{issue.severity}] {issue.category}")
                print(f"  File: {issue.file.relative_to(PROJECT_ROOT)}:{issue.line}")
                print(f"  Link: [{issue.link_text}]({issue.link_target})")
                print(f"  Error: {issue.error}")
                if issue.auto_fix:
                    print(f"  Auto-fix: {issue.auto_fix} (confidence: {issue.confidence:.0%})")

        # Status
        print("\n" + "=" * 80)
        if result.has_failures():
            print("[ERROR] Validation failed")
            print(f"Summary: {result.critical_errors + result.errors + result.warnings} issues")
        else:
            print("[OK] All links valid")
        print("=" * 80 + "\n")

    @staticmethod
    def json_report(result: ValidationResult, output_path: Path):
        """Generate JSON report."""
        report = {
            'summary': {
                'total_files': result.total_files,
                'total_links': result.total_links,
                'internal_links': result.internal_links,
                'external_links': result.external_links,
                'critical_errors': result.critical_errors,
                'errors': result.errors,
                'warnings': result.warnings,
                'info': result.info,
                'orphaned_files': len(result.orphaned_files),
                'duration_seconds': result.duration(),
                'timestamp': result.start_time.isoformat() if result.start_time else None,
            },
            'issues': [
                {
                    'severity': issue.severity,
                    'category': issue.category,
                    'file': str(issue.file.relative_to(PROJECT_ROOT)),
                    'line': issue.line,
                    'link_text': issue.link_text,
                    'link_target': issue.link_target,
                    'error': issue.error,
                    'auto_fix': issue.auto_fix,
                    'confidence': issue.confidence,
                }
                for issue in result.issues
            ],
            'orphaned_files': [str(f.relative_to(PROJECT_ROOT)) for f in result.orphaned_files],
        }

        output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(f"[OK] JSON report written to {output_path}")

    @staticmethod
    def markdown_report(result: ValidationResult) -> str:
        """Generate markdown report for GitHub comments."""
        status = "[ERROR] Failed" if result.has_failures() else "[OK] Passed"

        report = f"""## Link Validation Report

**Status**: {status}

**Summary**:
- Files: {result.total_files}
- Links: {result.total_links} ({result.internal_links} internal, {result.external_links} external)
- Issues: {result.critical_errors + result.errors + result.warnings} ({result.critical_errors} critical, {result.errors} errors, {result.warnings} warnings)
- Duration: {result.duration():.1f}s

"""

        if result.critical_errors > 0:
            report += "### [CRITICAL] Broken Internal Links\n\n"
            report += "| File | Line | Link | Error |\n"
            report += "|------|------|------|-------|\n"

            for issue in result.issues:
                if issue.severity == 'CRITICAL':
                    file_rel = issue.file.relative_to(PROJECT_ROOT)
                    report += f"| `{file_rel}` | {issue.line} | `{issue.link_target}` | {issue.error} |\n"

        return report


# ============================================================================
# Main Validator
# ============================================================================

class DocumentationValidator:
    """Main validation orchestrator."""

    def __init__(self, docs_root: Path, project_root: Path, mode: str = 'fast'):
        self.docs_root = docs_root
        self.project_root = project_root
        self.mode = mode
        self.extractor = LinkExtractor()
        self.validator = LinkValidator(docs_root, project_root, self.extractor)
        self.url_validator = ExternalURLValidator() if mode == 'external' else None
        self.orphan_detector = OrphanDetector(docs_root, EXCLUDE_FILES)

    def find_markdown_files(self, incremental: bool = False) -> List[Path]:
        """Find all markdown files to validate."""
        files = []

        # Docs directory
        for ext in ['*.md', '*.MD']:
            files.extend([f for f in self.docs_root.rglob(ext) if not any(ex in f.parts for ex in EXCLUDE_DIRS)])

        # Project directory (if not incremental)
        if not incremental:
            project_dir = self.project_root / ".project"
            for ext in ['*.md', '*.MD']:
                files.extend([f for f in project_dir.rglob(ext) if not any(ex in f.parts for ex in EXCLUDE_DIRS)])

        # TODO: Implement incremental mode (git diff)

        return files

    def validate(self, incremental: bool = False, detect_orphans: bool = True) -> ValidationResult:
        """Run full validation."""
        result = ValidationResult()
        result.start_time = datetime.now()

        print(f"[INFO] Starting validation (mode: {self.mode})")

        # Find files
        files = self.find_markdown_files(incremental)
        result.total_files = len(files)
        print(f"[INFO] Found {len(files)} markdown files")

        # Extract links
        print("[INFO] Extracting links...")
        all_links = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS_FILES) as executor:
            futures = {executor.submit(self.extractor.extract_links, f): f for f in files}

            for future in as_completed(futures):
                try:
                    links = future.result()
                    all_links.extend(links)
                except Exception as e:
                    file_path = futures[future]
                    print(f"[WARNING] Error extracting from {file_path}: {e}")

        result.total_links = len(all_links)
        result.internal_links = sum(1 for link in all_links if link.link_type != 'external')
        result.external_links = sum(1 for link in all_links if link.link_type == 'external')

        print(f"[INFO] Extracted {len(all_links)} links ({result.internal_links} internal, {result.external_links} external)")

        # Validate internal links
        print("[INFO] Validating internal links...")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS_FILES) as executor:
            futures = {executor.submit(self.validator.validate_link, link): link for link in all_links if link.link_type != 'external'}

            for future in as_completed(futures):
                try:
                    issue = future.result()
                    if issue:
                        result.add_issue(issue)
                except Exception as e:
                    link = futures[future]
                    print(f"[WARNING] Error validating {link.link_target}: {e}")

        # Validate external URLs (if enabled)
        if self.mode == 'external' and self.url_validator:
            print(f"[INFO] Validating {result.external_links} external URLs (this may take several minutes)...")

            external_links = [link for link in all_links if link.link_type == 'external']

            with ThreadPoolExecutor(max_workers=MAX_WORKERS_URLS) as executor:
                futures = {executor.submit(self.url_validator.validate_url, link): link for link in external_links}

                for i, future in enumerate(as_completed(futures), 1):
                    try:
                        issue = future.result()
                        if issue:
                            result.add_issue(issue)

                        # Rate limiting
                        if i % 10 == 0:
                            print(f"  [{i}/{result.external_links}] URLs checked...")
                        time.sleep(URL_RATE_LIMIT)

                    except Exception as e:
                        link = futures[future]
                        print(f"[WARNING] Error validating {link.link_target}: {e}")

        # Detect orphans
        if detect_orphans:
            print("[INFO] Detecting orphaned files...")
            self.orphan_detector.build_link_graph(all_links)
            result.orphaned_files = self.orphan_detector.find_orphans(files)

        result.end_time = datetime.now()
        print(f"[OK] Validation complete in {result.duration():.1f}s")

        return result


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive documentation link validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Validation modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--fast', action='store_true',
                           help='Fast mode: internal links only (~10s)')
    mode_group.add_argument('--full', action='store_true',
                           help='Full mode: all validation except external URLs (~30s)')
    mode_group.add_argument('--external', action='store_true',
                           help='External mode: includes HTTP validation (~3min)')

    # Auto-fix
    parser.add_argument('--fix', action='store_true',
                       help='Enable auto-fix mode')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview fixes without applying (requires --fix)')
    parser.add_argument('--apply', action='store_true',
                       help='Apply fixes (requires --fix)')

    # Orphan cleanup
    parser.add_argument('--cleanup-orphans', action='store_true',
                       help='Interactive orphan file cleanup')

    # Output options
    parser.add_argument('--output', type=Path,
                       help='Write JSON report to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output with detailed issues')
    parser.add_argument('--incremental', action='store_true',
                       help='Validate only changed files (git diff)')
    parser.add_argument('--no-orphans', action='store_true',
                       help='Skip orphan detection')

    args = parser.parse_args()

    # Determine mode
    if args.external:
        mode = 'external'
    elif args.fast:
        mode = 'fast'
    else:
        mode = 'full'

    # Validate arguments
    if args.apply and not args.fix:
        parser.error('--apply requires --fix')
    if args.dry_run and not args.fix:
        parser.error('--dry-run requires --fix')

    # Run validation
    validator = DocumentationValidator(DOCS_ROOT, PROJECT_ROOT, mode=mode)
    result = validator.validate(
        incremental=args.incremental,
        detect_orphans=not args.no_orphans
    )

    # Apply fixes
    if args.fix:
        dry_run = not args.apply
        fixer = AutoFixer(dry_run=dry_run)

        print(f"\n[INFO] Auto-fix mode ({'dry-run' if dry_run else 'applying'})")
        fixes = fixer.apply_fixes(result.issues)

        for file_path, file_fixes in fixes.items():
            print(f"\n{file_path.relative_to(PROJECT_ROOT)}:")
            for fix in file_fixes:
                print(f"  {fix}")

        print(f"\n[OK] Fixes applied: {fixer.fixes_applied}, failed: {fixer.fixes_failed}")

    # Cleanup orphans
    if args.cleanup_orphans and result.orphaned_files:
        stats = validator.orphan_detector.interactive_cleanup(
            result.orphaned_files,
            dry_run=args.dry_run
        )
        print(f"\n[INFO] Orphan cleanup: {stats}")

    # Generate reports
    ReportGenerator.console_report(result, verbose=args.verbose)

    if args.output:
        ReportGenerator.json_report(result, args.output)

    # Exit code (strict mode: fail on any warnings)
    if result.has_failures():
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
