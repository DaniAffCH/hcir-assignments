
from typing import Any
from enum import Enum
import numpy as np

class FaceClasses(Enum):
    UNAUTHORIZED = 0
    DANIELE = 1
    KLARA = 2

class FaceRecognition():
    def __init__(self) -> None:
        pass

    def __call__(self, img: np.ndarray) -> Any:
        return FaceClasses.UNAUTHORIZED # Hardcoded for now 