"""
QA-02: Main Entry Points Quality Audit Script
Multi-file batch audit for 4 main documentation entry points
Based on QA-01 methodology (NAVIGATION.md)
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Project root
PROJECT_ROOT = Path("D:/Projects/main")

# QA-02 Target Files
QA02_FILES = [
    {
        "path": PROJECT_ROOT / "docs/index.md",
        "type": "sphinx_index",
        "name": "docs/index.md",
        "description": "Sphinx homepage"
    },
    {
        "path": PROJECT_ROOT / "docs/guides/INDEX.md",
        "type": "guides_hub",
        "name": "guides/INDEX.md",
        "description": "User guides hub"
    },
    {
        "path": PROJECT_ROOT / "README.md",
        "type": "github_readme",
        "name": "README.md",
        "description": "GitHub entry point"
    },
    {
        "path": PROJECT_ROOT / "CLAUDE.md",
        "type": "team_memory",
        "name": "CLAUDE.md",
        "description": "Team memory"
    }
]

def analyze_completeness(content: str, lines: List[str], file_type: str) -> Dict:
    """Analyze completeness of file (file-type specific)."""
    issues = []

    # File-type specific checks
    if file_type == "sphinx_index":
        # Check for toctree directives
        toctree_count = len(re.findall(r'```{toctree}', content))
        if toctree_count < 5:
            issues.append({
                "line": None,
                "severity": "major",
                "issue": f"Only {toctree_count} toctrees found (expected ~11)",
                "impact": "Incomplete navigation structure"
            })

    elif file_type == "guides_hub":
        # Check for learning paths
        paths_found = len(re.findall(r'Path \d', content))
        if paths_found < 4:
            issues.append({
                "line": None,
                "severity": "major",
                "issue": f"Only {paths_found} learning paths found (expected 4-5)",
                "impact": "Incomplete learning path coverage"
            })

    elif file_type == "github_readme":
        # Check for standard README sections
        required_sections = ["Installation", "Usage", "Contributing", "License"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append({
                    "line": None,
                    "severity": "major",
                    "issue": f"Missing section: {section}",
                    "impact": "Incomplete README structure"
                })

    elif file_type == "team_memory":
        # Check for major sections (at least 15)
        section_count = len(re.findall(r'^##\s+\d+\)', content, re.MULTILINE))
        if section_count < 15:
            issues.append({
                "line": None,
                "severity": "minor",
                "issue": f"Only {section_count} numbered sections (expected ~23)",
                "impact": "May be missing content areas"
            })

    return {
        "score": max(0, 100 - len(issues) * 20),
        "issues": issues,
        "metrics": {
            "total_issues": len(issues)
        }
    }

def analyze_accuracy(content: str, lines: List[str], file_type: str) -> Dict:
    """Verify technical claims and file counts."""
    issues = []

    # Generic accuracy checks
    # Check for outdated dates (anything from 2024 or earlier in status sections)
    outdated_dates = re.findall(r'(?:Status|Updated|Date).*?202[0-4]', content, re.IGNORECASE)
    if outdated_dates:
        issues.append({
            "line": None,
            "severity": "minor",
            "issue": f"Found {len(outdated_dates)} potentially outdated dates",
            "impact": "Status information may be stale"
        })

    return {
        "score": max(0, 100 - len(issues) * 20),
        "issues": issues,
        "metrics": {
            "total_issues": len(issues)
        }
    }

def analyze_readability(content: str, lines: List[str]) -> Dict:
    """Analyze readability metrics (same as QA-01)."""
    issues = []

    # Filter out code blocks, tables, and Mermaid diagrams from readability analysis
    prose_lines = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
        elif not in_code_block and not stripped.startswith('|'):
            prose_lines.append(line)

    prose_content = '\n'.join(prose_lines)

    # Count sentences and words (only in prose, not code)
    sentences = re.split(r'[.!?]+', prose_content)
    total_sentences = len([s for s in sentences if s.strip()])

    # Calculate average sentence length
    words_per_sentence = []
    for sentence in sentences:
        if sentence.strip():
            words = len(sentence.split())
            words_per_sentence.append(words)
            if words > 40:
                issues.append({
                    "line": None,
                    "severity": "minor",
                    "issue": f"Long sentence ({words} words): {sentence[:50]}...",
                    "impact": "Reduced readability"
                })

    avg_sentence_length = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0

    # Check for passive voice (simplified heuristic)
    passive_patterns = [
        r'\bis\s+\w+ed\b', r'\bare\s+\w+ed\b', r'\bwas\s+\w+ed\b',
        r'\bwere\s+\w+ed\b', r'\bbeen\s+\w+ed\b'
    ]
    passive_count = sum(len(re.findall(pattern, prose_content, re.IGNORECASE)) for pattern in passive_patterns)
    passive_percentage = (passive_count / total_sentences) * 100 if total_sentences > 0 else 0

    if passive_percentage > 10:
        issues.append({
            "line": None,
            "severity": "minor",
            "issue": f"High passive voice usage: {passive_percentage:.1f}%",
            "impact": "Reduced clarity and engagement"
        })

    # Check paragraph length (count lines between blank lines)
    # Filter out code blocks, tables, and Mermaid diagrams
    paragraphs = content.split('\n\n')
    long_paragraphs = []
    for i, para in enumerate(paragraphs):
        # Skip code blocks, tables, and Mermaid content
        if ('```' in para or
            para.strip().startswith('|') or
            'subgraph' in para or
            '-->' in para or
            '==>' in para or
            para.strip().startswith('    ')):
            continue
        para_lines = [l for l in para.split('\n') if l.strip() and not l.strip().startswith('#')]
        if len(para_lines) > 5:
            long_paragraphs.append(i)

    if len(long_paragraphs) > 3:
        issues.append({
            "line": None,
            "severity": "minor",
            "issue": f"{len(long_paragraphs)} paragraphs exceed 5 sentences",
            "impact": "Dense text blocks reduce scannability"
        })

    # Flesch Reading Ease (simplified approximation)
    total_words = sum(words_per_sentence)
    total_syllables = total_words * 1.5
    flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * (total_syllables / total_words) if total_words > 0 else 0

    if flesch_score < 60:
        issues.append({
            "line": None,
            "severity": "major",
            "issue": f"Low readability score: {flesch_score:.1f} (target: 60-70)",
            "impact": "Difficult for mixed audience"
        })

    return {
        "score": max(0, 100 - len(issues) * 15),
        "issues": issues,
        "metrics": {
            "avg_sentence_length": f"{avg_sentence_length:.1f} words",
            "passive_voice_pct": f"{passive_percentage:.1f}%",
            "flesch_reading_ease": f"{flesch_score:.1f}",
            "long_sentences": len([w for w in words_per_sentence if w > 40]),
            "dense_paragraphs": len(long_paragraphs)
        }
    }

def analyze_accessibility(content: str, lines: List[str]) -> Dict:
    """Check accessibility compliance (same as QA-01)."""
    issues = []

    # Check heading hierarchy
    headings = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('#'):
            level = len(re.match(r'^#+', line.strip()).group())
            headings.append((i, level, line.strip()))

    for i in range(1, len(headings)):
        prev_level = headings[i-1][1]
        curr_level = headings[i][1]
        if curr_level > prev_level + 1:
            issues.append({
                "line": headings[i][0],
                "severity": "major",
                "issue": f"Heading hierarchy skip: H{prev_level} to H{curr_level}",
                "impact": "Screen readers cannot navigate properly"
            })

    # Check for Unicode emoji (ASCII-only rule)
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]')
    for i, line in enumerate(lines, 1):
        if emoji_pattern.search(line):
            issues.append({
                "line": i,
                "severity": "critical",
                "issue": f"Unicode emoji found: {line[:50]}",
                "impact": "Violates ASCII-only rule, breaks Windows terminal"
            })

    # Check for ASCII emoji markers (should be present but are still Unicode)
    ascii_markers = re.findall(r'[✅⏸️🔴🔵🟢🟡]', content)
    if ascii_markers:
        for i, line in enumerate(lines, 1):
            if any(marker in line for marker in ascii_markers):
                issues.append({
                    "line": i,
                    "severity": "critical",
                    "issue": f"Unicode emoji/marker found (not ASCII): {line[:50]}",
                    "impact": "VIOLATES CLAUDE.md CRITICAL RULE - Windows terminal incompatible"
                })

    # Check code blocks for language tags (only opening tags)
    in_code_block = False
    opening_tags = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not in_code_block:
                lang_tag = line.strip()[3:].strip()
                opening_tags.append((i, lang_tag))
                in_code_block = True
            else:
                in_code_block = False

    unlabeled_blocks = [(i, tag) for i, tag in opening_tags if not tag]
    if unlabeled_blocks:
        issues.append({
            "line": None,
            "severity": "minor",
            "issue": f"{len(unlabeled_blocks)} code blocks without language tags",
            "impact": "Syntax highlighting and screen readers impaired"
        })

    return {
        "score": max(0, 100 - len(issues) * 20),
        "issues": issues,
        "metrics": {
            "heading_hierarchy_errors": len([i for i in issues if "hierarchy" in i["issue"]]),
            "unicode_emoji_violations": len([i for i in issues if "emoji" in i.get("issue", "").lower()]),
            "code_block_issues": len(unlabeled_blocks)
        }
    }

def validate_file_links(content: str, filepath: Path) -> Dict:
    """Validate that linked files exist."""
    issues = []

    # Extract all markdown links
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    links = link_pattern.findall(content)

    tested_links = []
    broken_links = []

    for link_text, link_path in links[:20]:  # Test first 20 links
        # Skip external URLs
        if link_path.startswith('http'):
            continue

        # Skip anchors
        if link_path.startswith('#'):
            continue

        # Handle relative paths
        if link_path.startswith('../'):
            full_path = filepath.parent / link_path
        else:
            full_path = filepath.parent / link_path

        # Remove anchors
        full_path = Path(str(full_path).split('#')[0])

        tested_links.append(link_path)

        if not full_path.exists():
            broken_links.append(link_path)
            issues.append({
                "line": None,
                "severity": "critical",
                "issue": f"Broken link: {link_path}",
                "impact": "Navigation fails, user cannot access content"
            })

    return {
        "score": max(0, 100 - len(broken_links) * 10),
        "issues": issues,
        "tested_links": tested_links,
        "broken_links": broken_links,
        "metrics": {
            "links_tested": len(tested_links),
            "broken_links": len(broken_links)
        }
    }

def audit_single_file(file_info: Dict) -> Dict:
    """Audit a single file."""
    filepath = file_info["path"]
    file_type = file_info["type"]

    print(f"[INFO] Auditing {file_info['name']}...")

    # Check if file exists
    if not filepath.exists():
        return {
            "file": str(filepath),
            "name": file_info["name"],
            "type": file_type,
            "description": file_info["description"],
            "error": f"File not found: {filepath}",
            "overall_score": 0
        }

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return {
            "file": str(filepath),
            "name": file_info["name"],
            "type": file_type,
            "description": file_info["description"],
            "error": f"Error reading file: {e}",
            "overall_score": 0
        }

    # Run analysis tasks
    completeness = analyze_completeness(content, lines, file_type)
    accuracy = analyze_accuracy(content, lines, file_type)
    readability = analyze_readability(content, lines)
    accessibility = analyze_accessibility(content, lines)
    link_validation = validate_file_links(content, filepath)

    # Calculate overall score
    overall = (
        completeness["score"] +
        accuracy["score"] +
        readability["score"] +
        accessibility["score"] +
        link_validation["score"]
    ) / 5

    return {
        "file": str(filepath),
        "name": file_info["name"],
        "type": file_type,
        "description": file_info["description"],
        "file_stats": {
            "size_chars": len(content),
            "size_lines": len(lines),
            "size_kb": len(content) / 1024
        },
        "completeness": completeness,
        "accuracy": accuracy,
        "readability": readability,
        "accessibility": accessibility,
        "link_validation": link_validation,
        "overall_score": overall
    }

def main():
    """Main QA-02 audit function."""
    print("[INFO] Starting QA-02: Main Entry Points Audit...\n")

    # Audit all files
    results = []
    for file_info in QA02_FILES:
        result = audit_single_file(file_info)
        results.append(result)

        # Save individual result
        output_dir = Path("D:/Projects/main/.artifacts/qa_audits/individual_results")
        output_dir.mkdir(parents=True, exist_ok=True)

        individual_file = output_dir / f"{file_info['type']}_results.json"
        with open(individual_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        print(f"[OK] {file_info['name']}: {result.get('overall_score', 0):.1f}/100\n")

    # Calculate overall QA-02 score
    overall_qa02_score = sum(r.get("overall_score", 0) for r in results) / len(results)

    # Rank files by score (worst first = highest priority)
    ranked = sorted(results, key=lambda r: r.get("overall_score", 0))

    # Compile final report
    final_report = {
        "qa02_audit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overall_qa02_score": overall_qa02_score,
        "files_audited": len(results),
        "results": results,
        "ranked_priority": [
            {
                "priority": i + 1,
                "name": r["name"],
                "score": r.get("overall_score", 0),
                "description": r["description"]
            }
            for i, r in enumerate(ranked)
        ]
    }

    # Save JSON report
    output_file = Path("D:/Projects/main/.artifacts/qa_audits/qa_02_audit_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2)

    print(f"\n[OK] Results saved to {output_file}")
    print(f"\n{'='*60}")
    print(f"[SUMMARY] QA-02 Overall Score: {overall_qa02_score:.1f}/100")
    print(f"{'='*60}\n")

    # Print individual scores
    print("Individual File Scores:")
    for r in results:
        print(f"  {r['name']:20s} {r.get('overall_score', 0):6.1f}/100")

    print(f"\nPriority Ranking (fix worst first):")
    for i, r in enumerate(ranked, 1):
        print(f"  {i}. {r['name']:20s} {r.get('overall_score', 0):6.1f}/100")

    return results, overall_qa02_score

if __name__ == "__main__":
    main()
