from typing import Any
from model.face_recognition import FaceRecognition, FaceClasses
import time
import cv2
from BMLparser import Parser
from utils_ import PepperStates, Request
from speech.recognition import SpeechRecognition
from conversationEngine import ConversationEngine
from inferenceEngine import InferenceEngine
from rasaInterface import RasaInterface
import numpy as np

import random

# Main Idea: every state has a FSM associated 
class RecognitionFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.ts = None
        self.userDetected = None
        self.detectionThreshold = 0.7
        self.video_capture = cv2.VideoCapture(0)
        self.collectingTime = 10
        self.thePepperCoordinator = thePepperCoordinator
    
    def showImg(self, img, box, classification):
        img = np.array(img)
        if box is not None and classification is not None:
            img = cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
            img = cv2.putText(img, classification.name, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow("Detection", img)
        cv2.waitKey(1)


    def __call__(self) -> Any:
        match self.state:
            case 0:
                self.thePepperCoordinator.addRequest("sayGesture", {"text": f"Hi! My name is dorm buddy and I can help students to find a dorm. Let's see if I can recognize you!"})
                self.state = 1
            case 1:
                if self.ts is None:
                    self.faceDetections = list()
                    self.ts = time.time()
                # acquire img
                _, frame = self.video_capture.read()
                # inference 
                res, box = self.thePepperCoordinator.faceRecognition(frame)
                self.showImg(frame, box, res)
                # prediction
                self.faceDetections.append(res)

                if time.time() - self.ts > self.collectingTime:
                    cv2.destroyAllWindows()
                    self.ts = None
                    self.state = 2
            
            case 2:
                # threshold based on statistical analysis
                l = len(self.faceDetections)
                pd = self.faceDetections.count(FaceClasses.DANIELE) 
                pk = self.faceDetections.count(FaceClasses.KLARA) 
                pu = self.faceDetections.count(FaceClasses.UNAUTHORIZED)

                m = max([pd, pk, pu])
                
                if m == pd and pd > 5:
                    self.userDetected = FaceClasses.DANIELE
                    self.state = 4 if pd/l > self.detectionThreshold else 3

                elif m == pk and pk > 5:
                    self.userDetected = FaceClasses.KLARA
                    self.state = 4 if pk/l > self.detectionThreshold else 3

                elif m == pu:
                    self.userDetected = FaceClasses.UNAUTHORIZED
                    self.state = 5

            case 3:
                user = 'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'
                self.thePepperCoordinator.addRequest("notSure", {"text": f"I'm not sure about who you are. Are you {user}?"})
                
                sentiment, sentence = self.thePepperCoordinator.speechRecognition.listenAndGetSentiment()
                if sentiment == "no" or sentiment is None:
                    self.userDetected = None
                    self.thePepperCoordinator.addRequest("sayGesture", {"text": f"Ok I'm going to look at you more carefully"}, True)
                    self.state = 1
                elif sentiment == "yes":
                    self.state = 4

            case 4:
                user = 'Daniele' if self.userDetected == FaceClasses.DANIELE else 'Klara'
                self.thePepperCoordinator.addRequest("hello", {"name": user})
                self.state = 5 #DEAD STATE
                self.thePepperCoordinator.setState(PepperStates.CONVERSATION)

            case 5:
                self.thePepperCoordinator.addRequest("agreeGesture", {"text": f"I could not detect an authorized face."})
                self.thePepperCoordinator.addRequest("notSure", {"text": f"Let's try again."})
                self.state = 1

class ConversationFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.thePepperCoordinator = thePepperCoordinator
        self.shortAnsExpected = False
    
    def __call__(self) -> Any:
        match self.state:
            case 0:
                # General conversation!
                waitingTime = 4 if self.shortAnsExpected else 7
                sentence = self.thePepperCoordinator.speechRecognition.listen(waitingTime)
                answ = self.thePepperCoordinator.conversationEngine(sentence, verbose=True)
                self.thePepperCoordinator.addRequest("sayGesture", {"text": answ})
                self.shortAnsExpected = self.thePepperCoordinator.conversationEngine.shortAnswerExpected(answ)

                if self.thePepperCoordinator.conversationEngine.formCompleted(answ):
                    self.state = 1
                elif self.thePepperCoordinator.conversationEngine.earlyEnd(answ):
                    self.thePepperCoordinator.setState(PepperStates.FAREWELL)
               
            case 1:
                self.state = 0
                self.thePepperCoordinator.setState(PepperStates.INFERENCE)


class InferenceFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.thePepperCoordinator = thePepperCoordinator

    def __call__(self) -> Any:
        match self.state:
            case 0:
                form = RasaInterface.getSlotValues()

                self.sortedPreferences = self.thePepperCoordinator.inferenceEngine(str(form['limited_budget']),
                                                                                   str(form['willing_share']),
                                                                                   str(form['pay_more_for_private']),
                                                                                   str(form['uni_location']))
                self.state = 1
            case 1:
                if len(self.sortedPreferences) == 0:
                    self.thePepperCoordinator.addRequest("sayGesture", {"text": f"Unfortunately I proposed you all the dormitories I know and I don't have any other alternative to suggest."})
                    self.state = 0
                    self.thePepperCoordinator.setState(PepperStates.FAREWELL)
                else:
                    dormText = str(self.sortedPreferences[0][0])
                    print(self.sortedPreferences[0])
                    self.thePepperCoordinator.addRequest("agreeGesture", {"text": {dormText}})
                    self.thePepperCoordinator.addRequest("sayGesture", {"text":"Are you satisfied with this dorm?"})
                    sentiment, _ = self.thePepperCoordinator.speechRecognition.listenAndGetSentiment()
                    if sentiment == "yes":
                        self.state = 0
                        self.thePepperCoordinator.setState(PepperStates.FAREWELL)
                    else:
                        self.thePepperCoordinator.addRequest("notSure", {"text": f"Okay, no problem. I will find an alternative for you!"})
                        self.sortedPreferences.pop(0)


class FarewellFSM():
    def __init__(self, thePepperCoordinator) -> None:
        self.state = 0
        self.thePepperCoordinator = thePepperCoordinator

    def __call__(self) -> Any:
        match self.state:
            case 0:
                self.thePepperCoordinator.addRequest("agreeGesture", {"text": f"Can I help you with something else?"})
                sentiment, _ = self.thePepperCoordinator.speechRecognition.listenAndGetSentiment()
                if sentiment == "yes":
                    self.thePepperCoordinator.setState(PepperStates.CONVERSATION)
                else:
                    self.state = 1
            case 1:
                self.thePepperCoordinator.addRequest("bml_goodbye")
                self.state = 2 # DEAD STATE FOREVER

class PepperCoordinator():
    def __init__(self, pepper) -> None:

        self.stateToFSM = {
            PepperStates.RECOGNITION: RecognitionFSM(self),
            PepperStates.CONVERSATION: ConversationFSM(self),
            PepperStates.INFERENCE: InferenceFSM(self),
            PepperStates.FAREWELL: FarewellFSM(self)
        }
        self.loading(pepper)
        self.setState(PepperStates.RECOGNITION)


    def loading(self, pepper):
        self.bmlParser = Parser(pepper)
        self.speechRecognition = SpeechRecognition()
        self.faceRecognition = FaceRecognition("model/finetuned.pt")
        self.conversationEngine = ConversationEngine()
        self.inferenceEngine = InferenceEngine()


    def update(self):
        self.currentFSM()

    def setState(self, newState):
        self.currentFSM = self.stateToFSM[newState]
        self.state = newState

    def addRequest(self, name, params=None, async_=False):
        r = Request(name, params, async_)
        self.bmlParser.request(r)

