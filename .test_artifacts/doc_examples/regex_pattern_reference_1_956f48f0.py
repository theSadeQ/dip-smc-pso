# Example from: docs\tools\regex_pattern_reference.md
# Index: 1
# Runnable: True
# Hash: 956f48f0

THEOREM_PATTERN = re.compile(
    r'\*\*(?P<type>Theorem|Lemma|Proposition|Corollary)\s+(?P<number>\d+)\*\*'  # Type + number
    r'(?:\s*\((?P<title>[^)]+)\))?'                                              # Optional title
    r'(?:\s*\{cite\}`(?P<cite>[^`]+)`)?'                                         # Optional citation
    r'\s*(?P<statement>.*?)'                                                      # Statement text
    r'(?=\n\n|\*\*Proof)',                                                        # Stop at proof/blank
    re.DOTALL | re.MULTILINE
)