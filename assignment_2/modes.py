import threading
import time 
from abc import ABC, abstractmethod
from behaviourRealizer import BehaviorRealizer

class BehaviourClass(threading.Thread, ABC):
    def __init__(self, behaviourSeq, pepper):
        super(BehaviourClass, self).__init__()
        self.behaviourSeq = behaviourSeq
        self.behaviourRealizer = BehaviorRealizer(pepper)
        self.start_t = time.time()

    def run(self):
        while True:
            self.t = time.time() - self.start_t
            print(self.t)
            if self.behaviourSeq and self.behaviourSeq[0]["start"] <= self.t:
                element = self.behaviourSeq.pop(0)
                self.routine(element)

    @abstractmethod
    def routine(self, atomicBehaviour):
        pass

class Gesture(BehaviourClass):
    def routine(self, atomicBehaviour):
        self.behaviourRealizer.waving(atomicBehaviour["end"] - atomicBehaviour["start"])

class Speech(BehaviourClass):
    def routine(self, atomicBehaviour):
        self.behaviourRealizer.say(atomicBehaviour["text"])

class Gaze(BehaviourClass):
    def routine(self, atomicBehaviour):
        print("GAZE STARTED")

class Head(BehaviourClass):
    def routine(self, atomicBehaviour):
        print("HEAD STARTED")

class Posture(BehaviourClass):
    def routine(self, atomicBehaviour):
        print("POSTURE STARTED")