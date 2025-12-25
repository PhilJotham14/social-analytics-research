import math
from typing import List


def compute_score_raw(post_count: int, interactions: int) -> float:
    pc_log = math.log1p(post_count)
    ui_log = math.log1p(interactions)
    return 0.3 * pc_log + 0.7 * ui_log


def minmax_normalize(values: List[float]) -> List[float]:
    if not values:
        return []
    vmin = min(values)
    vmax = max(values)
    if math.isclose(vmin, vmax):
        return [0.0 for _ in values]
    return [100.0 * (v - vmin) / (vmax - vmin) for v in values]
