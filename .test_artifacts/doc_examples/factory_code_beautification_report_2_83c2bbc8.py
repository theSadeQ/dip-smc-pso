# Example from: docs\reports\factory_code_beautification_report.md
# Index: 2
# Runnable: False
# Hash: 83c2bbc8

# example-metadata:
# runnable: false

# Standard library imports (grouped and sorted)
import logging
import threading
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Protocol, TypeVar

# Third-party imports (version-aware)
import numpy as np
from numpy.typing import NDArray

# Local imports (hierarchical organization)
from src.core.dynamics import DIPDynamics
from src.controllers.smc.algorithms.classical.controller import ModularClassicalSMC