from dataclasses import dataclass
from typing import Callable
from .feature_context import feature_context
from . import features

@dataclass
class FeatureSpec:
    name: str
    func: Callable[[feature_context], float]
    weight: float

FEATURES = [
    FeatureSpec("remove_nine", features.feature_remove_nine, weight = 1.0),
    
]