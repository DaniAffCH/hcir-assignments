from enum import Enum
from typing import Any
from model.face_recognition import FaceRecognition, FaceClasses
import time
import cv2

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
        self.model = FaceRecognition()
        self.ts = None
        self.userDetected = None
        self.detectionThreshold = 0.4
        self.video_capture = cv2.VideoCapture(0)
        self.collectingTime = 5


    def __call__(self) -> Any:
        match self.state:
            case 0:
                if self.ts is None:
                    self.faceDetections = list()
                    self.ts = time.time()

                # acquire img
                _, frame = self.video_capture.read()
                # inference 
                res = self.model(frame)
                # prediction
                self.faceDetections.append(res)

                print("Collecting...")

                if time.time() - self.ts > self.collectingTime:
                    self.ts = None
                    self.state = 1
            
            case 1:
                print("Evaluating...")

                # thershold based on statistical analysis
                l = len(self.faceDetections)
                pd = self.faceDetections.count(FaceClasses.DANIELE) 
                pk = self.faceDetections.count(FaceClasses.KLARA) 
                pu = self.faceDetections.count(FaceClasses.UNAUTHORIZED)

                m = max([pd, pk, pu])
                
                if m == pd:
                    self.userDetected = FaceClasses.DANIELE
                    self.state = 3 if pd/l > self.detectionThreshold else 2

                elif m == pk:
                    self.userDetected = FaceClasses.KLARA
                    self.state = 3 if pk/l > self.detectionThreshold else 2

                elif m == pu:
                    self.userDetected = FaceClasses.UNAUTHORIZED
                    self.state = 4


            case 2:
                # unsure -> pepper says smth and wait for user answer 
                print("I'm not sure")

            case 3:
                print(f"I'm sure, it's {'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'}")

            case 4:
                # We have a negative answer, maybe pepper can say smth and then go back to state 0
                print("Not authorized user detected")


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
            PepperStates.RECOGNITION: RecognitionFSM(),
            PepperStates.GREETING: GreetingFSM(),
            PepperStates.CONVERSATION: ConversationFSM(),
            PepperStates.INFERENCE: InferenceFSM(),
            PepperStates.FAREWELL: FarewellFSM()
        }

        self.currentFSM = self.stateToFSM[self.state]

    def update(self):
        self.currentFSM()
    