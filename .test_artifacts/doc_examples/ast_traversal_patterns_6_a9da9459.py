# Example from: docs\tools\ast_traversal_patterns.md
# Index: 6
# Runnable: False
# Hash: a9da9459

docstring = """
Implements super-twisting algorithm from Levant (2003).
Finite-time convergence proven in [12]. DOI: 10.1016/j.automatica.2003.09.014
"""

citations = extract_all_citations(docstring)
# [
#   {"type": "implements", "match": {"what": "super-twisting algorithm",
#                                     "source": "Levant (2003)"}, ...},
#   {"type": "numbered_cite", "match": {"ref": "12"}, ...},
#   {"type": "doi", "match": {"doi": "10.1016/j.automatica.2003.09.014"}, ...}
# ]