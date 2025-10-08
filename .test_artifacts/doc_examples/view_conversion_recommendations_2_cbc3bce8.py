# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 2
# Runnable: False
# Hash: cbc3bce8

# BEFORE
def get_statistics(self) -> Dict[str, Any]:
    stats = self._stats.copy()  # ❌ Defensive copy
    stats['miss_rate'] = self._missed / self._total
    return stats

# AFTER
def get_statistics(self) -> Dict[str, Any]:
    stats = self._stats  # ✅ Direct reference (no mutation after this point)
    stats['miss_rate'] = self._missed / self._total
    return stats