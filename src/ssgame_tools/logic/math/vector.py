import math
from typing import List

def get_vector_magnitude(v):
    x, y = v
    return math.sqrt(x**2 + y**2)

def vector_magnitude_is_over_threshold(vector: List[float], threshold: float) -> bool:
    get_vector_magnitude(vector) > threshold