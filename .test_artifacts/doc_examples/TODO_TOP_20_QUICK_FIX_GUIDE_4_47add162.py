# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 4
# Runnable: False
# Hash: 47add162

# example-metadata:
# runnable: false

class LeaveOneOut:
    """Leave-One-Out cross-validation iterator.

    Each sample is used once as test set while remaining samples form training set.
    Equivalent to KFold(n_splits=n) where n is number of samples.

    Warning: Computationally expensive for large datasets.

    Examples
    --------
    >>> loo = LeaveOneOut()
    >>> for train_idx, test_idx in loo.split(data):
    ...     assert len(test_idx) == 1  # Single sample test set
    """