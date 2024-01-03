import requests

PORT = 5005

class RasaInterface:
    def interact(msg):
        payload = {"sender":"user",
                    "message": msg}
        r = requests.post(f'http://localhost:{PORT}/webhooks/rest/webhook', json=payload)
        r = r.json()

        return ". ".join([e["text"] for e in r if "text" in e]) if r else None
            
    def getSlotValues():
        response_tracker = requests.get(f"http://localhost:{PORT}/conversations/user/tracker")
        final_tracker_state = response_tracker.json()

        slot_values = final_tracker_state.get("slots", {})
        return slot_values