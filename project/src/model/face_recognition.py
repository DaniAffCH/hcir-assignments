
from typing import Any
import numpy as np
from utils import FaceClasses

class FaceRecognition():
    def __init__(self) -> None:
        pass

    def __call__(self, img: np.ndarray) -> Any:
        return FaceClasses.UNAUTHORIZED # Hardcoded for now 