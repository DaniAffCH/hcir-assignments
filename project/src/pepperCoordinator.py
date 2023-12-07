from typing import Any
from model.face_recognition import FaceRecognition, FaceClasses
import time
import cv2
from BMLparser import Parser
from utils import PepperStates, Request

# Main Idea: every state has a FSM associated 
class RecognitionFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.model = FaceRecognition()
        self.ts = None
        self.userDetected = None
        self.detectionThreshold = 0.4
        self.video_capture = cv2.VideoCapture(0)
        self.collectingTime = 5
        self.thePepperCoordinator = thePepperCoordinator

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

                # threshold based on statistical analysis
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
                user = 'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'
                self.thePepperCoordinator.addRequest("hello", {"name": user})
                self.state = 5 #DEAD STATE FOR NOW, TODO: go to a different high level FSM

            case 4:
                print("Not authorized user detected")
                # We have a negative answer, maybe pepper can say smth and then go back to state 0
                self.thePepperCoordinator.addRequest("notOk")
                self.state = 5 #DEAD STATE FOR NOW, TODO: go back to state 0


class GreetingFSM(): # Is it really necessary?? 
    pass

class ConversationFSM():
    pass

class InferenceFSM():
    # Inference is the inference itself + answer. If the user it's not satisfied go back to conversation
    pass

class FarewellFSM():
    pass

class PepperCoordinator():
    def __init__(self, pepper) -> None:
        self.state = PepperStates.RECOGNITION

        self.stateToFSM = {
            PepperStates.RECOGNITION: RecognitionFSM(self),
            PepperStates.GREETING: GreetingFSM(),
            PepperStates.CONVERSATION: ConversationFSM(),
            PepperStates.INFERENCE: InferenceFSM(),
            PepperStates.FAREWELL: FarewellFSM()
        }
        self.bmlParser = Parser(pepper)
        self.currentFSM = self.stateToFSM[self.state]

    def update(self):
        self.currentFSM()

    def addRequest(self, name, params=None, async_=False):
        r = Request(name, params, async_)
        self.bmlParser.request(r)

