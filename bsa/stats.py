"""Confidence intervals. A rate without an interval is not published."""
from math import sqrt


def wilson(successes: int, runs: int, z: float = 1.959964) -> tuple[float, float]:
    """95% Wilson score interval for a proportion."""
    if runs <= 0 or not 0 <= successes <= runs:
        raise ValueError("need 0 <= successes <= runs and runs > 0")
    p = successes / runs
    z2 = z * z
    denom = 1 + z2 / runs
    centre = (p + z2 / (2 * runs)) / denom
    margin = z * sqrt(p * (1 - p) / runs + z2 / (4 * runs * runs)) / denom
    # The exact bound is 0 or 1 at the extremes; only floating point error can miss it.
    low = 0.0 if successes == 0 else max(0.0, centre - margin)
    high = 1.0 if successes == runs else min(1.0, centre + margin)
    return low, high


def clustered_mean(clusters: list[list[int]], z: float = 1.959964) -> dict:
    """Mean of 0/1 scores with a cluster-adjusted standard error (Miller 2024, arXiv 2411.00640, appendix A).

    Scores in one cluster are not independent, so their deviations are added before squaring.
    The interval is the paper's normal approximation, which is optimistic when clusters are few.
    """
    scores = [s for cluster in clusters for s in cluster]
    if not scores:
        raise ValueError("need at least one score")
    n = len(scores)
    mean = sum(scores) / n
    se = sqrt(sum(sum(s - mean for s in cluster) ** 2 for cluster in clusters)) / n
    return {"mean": mean, "se": se, "low": max(0.0, mean - z * se), "high": min(1.0, mean + z * se),
            "clusters": len(clusters), "items": n}
