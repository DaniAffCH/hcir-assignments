from BLMparser import Parser
from modes import Gesture, Speech, Gaze, Head, Posture
import threading
def dummy(i):
    for _ in range(100):
        print(f"hello i'm {i}")
class Coordinator():
    def __init__(self, parser:Parser) -> None:
        self.behaviours = parser.getBehaviours()
        self.threads = list()
        self.classMapping = {
            "gaze": Gaze,
            "speech": Speech,
            "gesture": Gesture,
            "head": Head,
            "posture": Posture
        }

    def spawn(self):
        for e in self.behaviours:
            if e not in self.classMapping:
                raise Exception("[Fatal] BLM syntax error, {e} is not a valid behavior type")
            tmp = self.classMapping[e](self.behaviours[e])
            tmp.start()
            self.threads.append(tmp)

    def join(self):
        for e in self.threads:
            e.join()