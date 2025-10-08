# Example from: docs\guides\api\utilities.md
# Index: 2
# Runnable: True
# Hash: e3e7ebc3

from src.utils.validation import check_numerical_health

state = np.array([0.1, 0.05, 0.2, 0.1, 0.25, 0.15])

health = check_numerical_health(state)

if not health['is_finite']:
    print("State contains NaN or Inf!")
if not health['is_bounded']:
    print("State values unreasonably large!")