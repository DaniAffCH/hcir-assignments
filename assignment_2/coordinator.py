from BLMparser import Parser
from modes import Gesture, Speech, Gaze, Head, Posture

class Coordinator():
    def __init__(self, parser:Parser, pepper) -> None:
        self.behaviours = parser.getBehaviours()
        self.threads = list()
        self.pepper = pepper
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
            tmp = self.classMapping[e](self.behaviours[e], self.pepper)
            tmp.start()
            self.threads.append(tmp)

    def join(self):
        for e in self.threads:
            e.join()
        self.threads = list()