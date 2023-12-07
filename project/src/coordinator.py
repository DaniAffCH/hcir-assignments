from modes import Gesture, Speech, Gaze, Head, Posture

class Coordinator():

    """
    A thread spawner class.

    ...

    Attributes
    ----------
    classMapping: dict
        maps type name into a class
    threads: list 
        list of threads
    pepper: qibullet.pepper_virtual.PepperVirtual
        pepper instance
    behaviours: dict 
        dictionary containing the bml attributes

    Methods
    -------
    spawn()
        it spawns a thread for every behavior mode, running the corresponding class.
    join()
        wait for all the threads to finish
    """

    def __init__(self, parser, pepper) -> None:
        self.threads = list()
        self.pepper = pepper
        self.parser = parser
        self.classMapping = {
            "gaze": Gaze,
            "speech": Speech,
            "gesture": Gesture,
            "head": Head,
            "posture": Posture
        }

    def spawn(self):
        self.behaviours = self.parser.getBehaviours()
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