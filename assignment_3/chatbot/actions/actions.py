# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


ENDPOINT = "https://openmensa.org/api/v2"
MENSA_ID = 24

class ActionMensa(Action):
    def name(self) -> Text:
        return "action_mensa"
    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        outStr = None

        url_request = f"{ENDPOINT}/canteens/{MENSA_ID}/days"
        res = requests.get(url_request)
        if res != None:
            data = res.json()
            recent_date = data[-1]["date"]
            url_request = f"{ENDPOINT}/canteens/{MENSA_ID}/days/{recent_date}/meals"
            res = requests.get(url_request)
            
            if res != None:
                data = res.json()
                outStr = "\n".join([f"• {item['name']}" for item in data])
                outStr = f"Here is today's menu:\n"+outStr

        if outStr is None:
            dispatcher.utter_message("Sorry, I could not get the mensa menu. Please try again.")
        else:
            dispatcher.utter_message(outStr)
        return []
