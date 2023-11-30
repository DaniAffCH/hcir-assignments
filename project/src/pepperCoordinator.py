from enum import Enum
from typing import Any

# Main Idea: every state has a FSM associated 
class PepperStates(Enum):
    RECOGNITION = 1
    GREETING = 2
    CONVERSATION = 3
    INFERENCE = 4
    FAREWELL = 5



class RecognitionFSM():
    def __init__(self) -> None:
        self.state = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class GreetingFSM():
    pass

class ConversationFSM():
    pass

class InferenceFSM():
    # Inference is the inference itself + answer. If the user it's not satisfied go back to conversation
    pass

class FarewellFSM():
    pass

class PepperCoordinator():
    def __init__(self) -> None:
        self.state = PepperStates.RECOGNITION

        self.stateToFSM = {
            PepperStates.RECOGNITION: RecognitionFSM,
            PepperStates.GREETING: GreetingFSM,
            PepperStates.CONVERSATION: ConversationFSM,
            PepperStates.INFERENCE: InferenceFSM,
            PepperStates.FAREWELL: FarewellFSM
        }

        self.currentFSM = self.stateToFSM[self.state]


    def update():
        pass
    