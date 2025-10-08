# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 5
# Runnable: False
# Hash: ed5c8c4a

# .coveragerc configuration
[run]
source = src
omit =
    */tests/*
    */conftest.py
    */__init__.py

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = coverage_html_report

[term]
missing = True
skip_covered = False