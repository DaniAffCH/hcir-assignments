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

        ack = "Ok, I will look for cheap solutions" if slot_value \
              else "Ok, I will consider every possibility then"

        dispatcher.utter_message(text=ack)
        return {"limited_budget": slot_value}
    
    def validate_willing_share(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        ack = "Got it! This helps to keep the price low" if slot_value \
              else "Got it! Let's look for a private accomodation"

        dispatcher.utter_message(text=ack)
        return {"willing_share": slot_value}
    
    def validate_pay_more_for_private(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        ack = "So you are willing to pay more, I will keep that in mind" if slot_value \
              else "So you prefer to share the dorm to pay less, I will keep that in mind"

        dispatcher.utter_message(text=ack)
        return {"pay_more_for_private": slot_value}
    
    def validate_uni_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        ack = f"Ok we will find something close to the {slot_value}"

        dispatcher.utter_message(text=ack)
        return {"uni_location": slot_value}
        

