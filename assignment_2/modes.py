import threading
import time 
from abc import ABC, abstractmethod
from behaviourRealizer import BehaviorRealizer

class BehaviourClass(threading.Thread, ABC):
    def __init__(self, behaviourSeq, pepper):
        super(BehaviourClass, self).__init__()
        self.behaviourSeq = behaviourSeq
        self.behaviourRealizer = BehaviorRealizer(pepper)

    def run(self):
        start_t = time.time()

        while True:
            t = time.time() - start_t
            if self.behaviourSeq and self.behaviourSeq[0]["start"] <= t:
                assert(self.behaviourSeq[0]["start"] < self.behaviourSeq[0]["end"])
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
        self.behaviourRealizer.lookAtRelativePoint(50,0,20,atomicBehaviour["end"] - atomicBehaviour["start"])

class Head(BehaviourClass):
    def routine(self, atomicBehaviour):
        self.behaviourRealizer.nod(atomicBehaviour["end"] - atomicBehaviour["start"])

class Posture(BehaviourClass):
    def routine(self, atomicBehaviour):
        self.behaviourRealizer.happySwirl(atomicBehaviour["end"] - atomicBehaviour["start"])