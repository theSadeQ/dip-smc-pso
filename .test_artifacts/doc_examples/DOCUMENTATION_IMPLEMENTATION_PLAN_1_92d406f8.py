# Example from: docs\DOCUMENTATION_IMPLEMENTATION_PLAN.md
# Index: 1
# Runnable: False
# Hash: 92d406f8

# example-metadata:
# runnable: false

   from typing import Tuple, Optional, Callable, Dict, List
   import numpy.typing as npt

   def f(state: npt.NDArray[np.float64], u: float) -> npt.NDArray[np.float64]:
       ...