# Example from: docs\tools\claim_extraction_guide.md
# Index: 14
# Runnable: True
# Hash: b2c6baf5

# For complex markdown, parse to AST instead of regex
from markdown_ast import parse_markdown

tree = parse_markdown(file_content)
theorems = [node for node in tree if node.type == "theorem"]