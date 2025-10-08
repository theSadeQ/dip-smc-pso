# Example from: docs\tools\claim_extraction_guide.md
# Index: 18
# Runnable: False
# Hash: c51edd35

# Add to code_extractor.py
import nbformat

def extract_from_notebook(notebook_path: str):
    nb = nbformat.read(notebook_path, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            # Extract from code cell source
            tree = ast.parse(cell.source)
            # ... (existing AST extraction)