from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ValidateDormForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_dorm_form"

    def validate_limited_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"OK! GOTCHA")
        return {"limited_budget": slot_value}

