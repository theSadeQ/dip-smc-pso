# Example from: docs\PHASE_1_2_VS_1_3_VALIDATION.md
# Index: 1
# Runnable: True
# Hash: e3ac38c3

# Phase 1.3 filter logic:
is_public = not method.name.startswith('_')
undoc_methods = sum(1 for m in all_methods if not m.docstring.has_docstring and m.is_public)