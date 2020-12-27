from typing import List


def mean(values: List[float]):
    count = len(values)
    result = sum(values) / count
    return result
