# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 3
# Runnable: False
# Hash: 2973a56e

class TimeSeriesSplit:
    """Time series cross-validation iterator.

    Respects temporal ordering by using past data for training and future data
    for validation. Prevents data leakage in time series forecasting tasks.

    Parameters
    ----------
    n_splits : int, default=5
        Number of splits.
    test_size : int, optional
        Size of test set. If None, uses remaining data.

    Examples
    --------
    >>> ts_split = TimeSeriesSplit(n_splits=3)
    >>> for train_idx, test_idx in ts_split.split(time_series_data):
    ...     # train_idx: [0, ..., t-1]
    ...     # test_idx: [t, ..., T]
    """