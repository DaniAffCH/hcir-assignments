from typing import Any
from model.face_recognition import FaceRecognition, FaceClasses
import time
import cv2
from BMLparser import Parser
from utils_ import PepperStates, Request
from speech.recognition import SpeechRecognition
from conversationEngine import ConversationEngine

# Main Idea: every state has a FSM associated 
class RecognitionFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.ts = None
        self.userDetected = None
        self.detectionThreshold = 0.7
        self.video_capture = cv2.VideoCapture(0)
        self.collectingTime = 5
        self.thePepperCoordinator = thePepperCoordinator

    def __call__(self) -> Any:
        match self.state:
            case 0:
                self.thePepperCoordinator.addRequest("say", {"text": f"Hi! I'm Pepper. Let's see if I can recognize you!"})
                self.state = 1
            case 1:
                if self.ts is None:
                    self.faceDetections = list()
                    self.ts = time.time()

                # acquire img
                _, frame = self.video_capture.read()
                
                # inference 
                res = self.thePepperCoordinator.faceRecognition(frame)
                # prediction
                self.faceDetections.append(res)

                if time.time() - self.ts > self.collectingTime:
                    self.ts = None
                    self.state = 2
            
            case 2:
                # threshold based on statistical analysis
                l = len(self.faceDetections)
                pd = self.faceDetections.count(FaceClasses.DANIELE) 
                pk = self.faceDetections.count(FaceClasses.KLARA) 
                pu = self.faceDetections.count(FaceClasses.UNAUTHORIZED)

                m = max([pd, pk, pu])
                
                if m == pd:
                    self.userDetected = FaceClasses.DANIELE
                    self.state = 4 if pd/l > self.detectionThreshold else 3

                elif m == pk:
                    self.userDetected = FaceClasses.KLARA
                    self.state = 4 if pk/l > self.detectionThreshold else 3

                elif m == pu:
                    self.userDetected = FaceClasses.UNAUTHORIZED
                    self.state = 5


            case 3:
                user = 'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'
                self.thePepperCoordinator.addRequest("say", {"text": f"I'm not sure about who you are. Are you {user}?"})
                sentiment, sentence = self.thePepperCoordinator.speechRecognition.listenAndGetSentiment()
                print(sentiment, sentence)
                if sentiment == "no" or sentiment is None:
                    self.userDetected = None
                    self.thePepperCoordinator.addRequest("say", {"text": f"Ok I'm going to look at you more carefully"}, True)
                    self.state = 1
                elif sentiment == "yes":
                    self.state = 4


            case 4:
                user = 'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'
                self.thePepperCoordinator.addRequest("hello", {"name": user})
                self.state = 5 
                self.thePepperCoordinator.setState(PepperStates.CONVERSATION)

            case 5:
                # We have a negative answer, maybe pepper can say smth and then go back to state 0
                self.thePepperCoordinator.addRequest("notOk")
                self.state = 1

class ConversationFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 1
        self.thePepperCoordinator = thePepperCoordinator

    def __call__(self) -> Any:
        match self.state:
            case 0:
                # General conversation!
                sentence = self.thePepperCoordinator.speechRecognition.listen(7)
                answ = self.thePepperCoordinator.conversationEngine(sentence, verbose=True)
                # Make something more engagin with gestures ecc ecc
                self.thePepperCoordinator.addRequest("say", {"text": answ})


            case 1:
                # Very short answer expected
                sentence = self.thePepperCoordinator.speechRecognition.listen(4)
                answ = self.thePepperCoordinator.conversationEngine(sentence, verbose=True)
                self.thePepperCoordinator.addRequest("say", {"text": answ})


class InferenceFSM():
    # Inference is the inference itself + answer. If the user it's not satisfied go back to conversation
    pass

class FarewellFSM():
    pass

class PepperCoordinator():
    def __init__(self, pepper) -> None:

        self.stateToFSM = {
            PepperStates.RECOGNITION: RecognitionFSM(self),
            PepperStates.CONVERSATION: ConversationFSM(self),
            PepperStates.INFERENCE: InferenceFSM(),
            PepperStates.FAREWELL: FarewellFSM()
        }
        self.loading(pepper)
        self.setState(PepperStates.RECOGNITION)


    def loading(self, pepper):
        self.bmlParser = Parser(pepper)
        self.speechRecognition = SpeechRecognition()
        self.conversationEngine = ConversationEngine()
        self.faceRecognition = FaceRecognition("model/trained_model.pt")

    def update(self):
        self.currentFSM()

    def setState(self, newState):
        self.currentFSM = self.stateToFSM[newState]
        self.state = newState

    def addRequest(self, name, params=None, async_=False):
        r = Request(name, params, async_)
        self.bmlParser.request(r)

