# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 3
# Runnable: False
# Hash: 72203d6a

# example-metadata:
# runnable: false

# Standard library imports (alphabetical)
from __future__ import annotations
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

# Third-party imports (alphabetical)
import numpy as np

# Local project imports (explicit)
from src.config import ConfigSchema, load_config
from src.utils.seed import create_rng