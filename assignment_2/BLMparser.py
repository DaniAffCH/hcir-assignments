import json 
import os

# TODO: every block is a class?

class Parser():
    def __init__(self, path:str) -> None:
        self.__sanityChecks(path)

        with open(path, "r") as f:
            self.rawJson = json.load(f)
        
        # Sort every behaviour category according its starting time
        for k in self.rawJson["bml"]["behaviours"]:
            self.rawJson["bml"]["behaviours"][k] = sorted(self.rawJson["bml"]["behaviours"][k], key=lambda e: e["start"])
        
    def __sanityChecks(self, path):
        if not os.path.exists(path):
            raise Exception(f"[FATAL] {path} does not exist")
        elif not path.endswith(".json") and not path.endswith(".JSON"):
            raise Exception(f"[FATAL] invalid extension")
        
    def getBehaviours(self):
        return self.rawJson["bml"]["behaviours"]
    
    def getRobotName(self):
        return self.rawJson["bml"]["character"]