from utils_ import Request
from coordinator import Coordinator
import json 
import os

BML_PATH = "bml"

# The Parser class is responsible for parsing and processing BML files, including
# performing sanity checks, sorting behaviours, filling templates, and coordinating
# the execution of behaviours.
class Parser():
    def __init__(self, pepper) -> None:
        self.modeCoordinator = Coordinator(self, pepper)

    def request(self, req:Request) -> None:
        path = os.path.join(BML_PATH, req.name+".json")
        self.__sanityChecks(path)

        with open(path, "r") as f:
            self.rawJson = json.load(f)
        
        # Sort every behaviour category according its starting time
        for k in self.rawJson["bml"]["behaviours"]:
            self.rawJson["bml"]["behaviours"][k] = sorted(self.rawJson["bml"]["behaviours"][k], key=lambda e: e["start"])

        # Fill templates if needed
        if req.params:
            for i, _ in enumerate(self.rawJson["bml"]["behaviours"]["speech"]):
                self.rawJson["bml"]["behaviours"]["speech"][i]["text"] = self.rawJson["bml"]["behaviours"]["speech"][i]["text"].format(**req.params)

        self.modeCoordinator.spawn()

        if not req.async_:
            self.modeCoordinator.join() 

        
    def __sanityChecks(self, path):
        if not os.path.exists(path):
            raise Exception(f"[FATAL] {path} does not exist")
        elif not path.endswith(".json") and not path.endswith(".JSON"):
            raise Exception(f"[FATAL] invalid extension")
        
    def getBehaviours(self):
        return self.rawJson["bml"]["behaviours"]
    
    def getRobotName(self):
        return self.rawJson["bml"]["character"]