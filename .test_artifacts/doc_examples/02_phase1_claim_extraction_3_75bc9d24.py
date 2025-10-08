# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 3
# Runnable: True
# Hash: 75bc9d24

import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FormalClaim:
    id: str
    type: str  # "theorem", "lemma", "proposition", "corollary"
    number: Optional[int]
    statement: str
    proof: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    confidence: float

class FormalClaimExtractor:
    PATTERNS = {
        'theorem_numbered': re.compile(
            r'\*\*(?P<type>Theorem|Lemma|Proposition|Corollary)\s+(?P<number>\d+)\*\*'
            r'(?:\s*\((?P<title>[^)]+)\))?'  # Optional title
            r'(?:\s*\{cite\}`(?P<cite>[^`]+)`)?'  # Existing citation
            r'\s*(?P<statement>.*?)'  # Statement text
            r'(?=\n\n|\*\*Proof)',  # Stop at proof or blank line
            re.DOTALL | re.MULTILINE
        ),
        'proof_block': re.compile(
            r'\*\*Proof\*\*:?\s*(?P<proof>.*?)(?P<qed>□|∎|QED)',
            re.DOTALL
        ),
        'math_block': re.compile(r'