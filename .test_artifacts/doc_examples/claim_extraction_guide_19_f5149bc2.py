# Example from: docs\tools\claim_extraction_guide.md
# Index: 19
# Runnable: True
# Hash: f5149bc2

from langdetect import detect

if detect(docstring) != 'en':
    docstring = translate_to_english(docstring)  # Use translation API