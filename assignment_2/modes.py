import threading
import time 
from abc import ABC, abstractmethod

class BehaviourClass(threading.Thread, ABC):
    def __init__(self, behaviourSeq):
        super(BehaviourClass, self).__init__()
        self.behaviourSeq = behaviourSeq

    def run(self):
        while True:
            self.t = time.time()
            self.routine()

    @abstractmethod
    def routine(self):
        pass

class Gesture(BehaviourClass):
    def __init__(self, behaviourSeq):
        super().__init__(behaviourSeq)

    def routine(self):
        print("GESTURE STARTED")

class Speech(BehaviourClass):
    def __init__(self, behaviourSeq):
        super().__init__(behaviourSeq)

    def routine(self):
        print("SPEECH STARTED")

class Gaze(BehaviourClass):
    def __init__(self, behaviourSeq):
        super().__init__(behaviourSeq)

    def routine(self):
        print("GAZE STARTED")

class Head(BehaviourClass):
    def __init__(self, behaviourSeq):
        super().__init__(behaviourSeq)

    def routine(self):
        print("HEAD STARTED")

class Posture(BehaviourClass):
    def __init__(self, behaviourSeq):
        super().__init__(behaviourSeq)

    def routine(self):
        print("POSTURE STARTED")