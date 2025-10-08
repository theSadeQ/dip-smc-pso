# Example from: docs\plans\documentation\week_1_completion_report.md
# Index: 1
# Runnable: False
# Hash: 8a1fddb4

# example-metadata:
# runnable: false

# Syntax highlighting style
pygments_style = 'monokai'  # Dark theme for code

# Literalinclude defaults
highlight_options = {
    'linenos': True,          # Show line numbers
    'linenostart': 1,         # Start from line 1
}

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_copybutton',      # Copy code button
    'myst_parser',            # Markdown support
    'sphinx_design',          # Design elements
]