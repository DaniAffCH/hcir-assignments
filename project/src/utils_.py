from dataclasses import dataclass
from enum import Enum

class PepperStates(Enum):
    RECOGNITION = 1
    GREETING = 2
    CONVERSATION = 3
    INFERENCE = 4
    FAREWELL = 5

class FaceClasses(Enum):
    UNAUTHORIZED = 0
    DANIELE = 1
    KLARA = 2

@dataclass
class Request:
    name: str
    params: dict
    async_: bool
    
@dataclass
class Dorms:
    name:str
    address:str
    location:str
    shared_common_areas:str
    prices:str

    def __str__(self) -> str:
        return f"{self.name} situated in {self.location}. The dorm offers {self.shared_common_areas}. The price of this dorm depends on the specific room you choose, but I can provide you a range: {self.prices}"