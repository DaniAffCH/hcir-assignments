import requests

PORT = 5005

class RasaInterface:
    def interact(msg):
        payload = {"sender":"user",
                    "message": msg}
        r = requests.post(f'http://localhost:{PORT}/webhooks/rest/webhook', json=payload)

        #metadata = requests.get("http://localhost:5005/conversations/default/tracker")
        #intents = metadata.json()["intent_ranking"]

        return r.json()[0]['text'] if r.json() else None
    