# Example from: docs\reports\test_infrastructure_analysis_report.md
# Index: 2
# Runnable: True
# Hash: da7dd3b1

#==========================================================================================\\\
#============== tests/test_utils/control/test_control_primitives.py =====================\\\
#==========================================================================================\\\

"""Tests for control utility primitives and saturation functions."""

import numpy as np
import pytest

from src.utils import saturate