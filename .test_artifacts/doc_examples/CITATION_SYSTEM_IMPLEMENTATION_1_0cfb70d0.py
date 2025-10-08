# Example from: docs\implementation_reports\CITATION_SYSTEM_IMPLEMENTATION.md
# Index: 1
# Runnable: False
# Hash: 0cfb70d0

# example-metadata:
# runnable: false

extensions = [
    # ... existing extensions
    "sphinxcontrib.bibtex",
]

bibtex_bibfiles = [
    "bib/smc.bib",
    "bib/pso.bib",
    "bib/dip.bib",
    "bib/software.bib",
]
bibtex_default_style = "unsrt"          # stable ordering
bibtex_reference_style = "label"        # renders [1], [2], ...
bibtex_tooltips = True
bibtex_bibliography_header = ".. rubric:: References"