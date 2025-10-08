# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 2
# Runnable: False
# Hash: 10a72dfd

# example-metadata:
# runnable: false

class StratifiedKFold:
    """Stratified K-Fold cross-validation iterator.

    Ensures each fold has approximately the same percentage of samples from each class.
    Useful for imbalanced classification tasks.

    Parameters
    ----------
    n_splits : int, default=5
        Number of folds.
    shuffle : bool, default=False
        Whether to shuffle data before splitting.
    random_state : int, optional
        Random seed for reproducibility.

    Examples
    --------
    >>> labels = [0, 0, 0, 1, 1, 1, 1, 1]  # Imbalanced
    >>> skfold = StratifiedKFold(n_splits=3, shuffle=True)
    >>> for train_idx, val_idx in skfold.split(data, labels):
    ...     # Each fold maintains class distribution
    """