# Example from: docs\plans\documentation\week_1_foundation_automation.md
# Index: 2
# Runnable: False
# Hash: 672333a0

# example-metadata:
# runnable: false

extensions = [
    'sphinx.ext.autodoc',           # Existing
    'sphinx.ext.napoleon',          # Existing
    'sphinx.ext.viewcode',          # Existing
    'sphinx.ext.literalinclude',    # NEW - Embed source code
    'sphinx.ext.githubpages',       # Existing
    'myst_parser',                  # Existing (Markdown support)
    'sphinx_copybutton',            # NEW - Copy code button
    'sphinx_togglebutton',          # NEW - Collapsible code blocks
    'sphinx_design',                # NEW - Better UI components
]