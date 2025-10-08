# Example from: docs\tools\ast_traversal_patterns.md
# Index: 8
# Runnable: True
# Hash: b36e5f93

import time
import ast
import re
from pathlib import Path

def benchmark_regex(file_path: str) -> float:
    """Regex-only approach (no AST)."""
    start = time.perf_counter()
    content = Path(file_path).read_text()

    for pattern in CITATION_PATTERNS.values():
        pattern.findall(content)  # Extract from entire file

    return time.perf_counter() - start

def benchmark_ast(file_path: str) -> float:
    """AST + regex hybrid approach."""
    start = time.perf_counter()
    content = Path(file_path).read_text()
    tree = ast.parse(content)

    extractor = CodeClaimExtractor()
    extractor.visit(tree)

    return time.perf_counter() - start