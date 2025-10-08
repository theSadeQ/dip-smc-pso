# Example from: docs\tools\regex_pattern_reference.md
# Index: 4
# Runnable: True
# Hash: a9184582

def extract_theorems(file_content):
    for line in file_content.split('\n'):
        pattern = re.compile(r'\*\*Theorem.*')  # ← Compile per line!
        match = pattern.search(line)