# Example from: docs\tools\claim_extraction_guide.md
# Index: 7
# Runnable: True
# Hash: f74c2c5b

# Add to code_extractor.py
import pickle
from pathlib import Path

def parse_with_cache(file_path: str):
    cache_path = Path(f".cache/{file_path}.ast")

    if cache_path.exists():
        return pickle.load(cache_path.open("rb"))

    tree = ast.parse(Path(file_path).read_text())
    cache_path.parent.mkdir(exist_ok=True)
    pickle.dump(tree, cache_path.open("wb"))
    return tree