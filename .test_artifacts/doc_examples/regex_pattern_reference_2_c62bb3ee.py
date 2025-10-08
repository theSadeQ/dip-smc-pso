# Example from: docs\tools\regex_pattern_reference.md
# Index: 2
# Runnable: True
# Hash: c62bb3ee

PROOF_PATTERN = re.compile(
    r'\*\*Proof\*\*:?\s*'          # "**Proof**" with optional colon
    r'(?P<proof>.*?)'               # Proof text (non-greedy)
    r'(?P<qed>□|∎|QED)',            # QED symbol (required)
    re.DOTALL
)