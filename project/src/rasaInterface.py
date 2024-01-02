import requests

PORT = 5005

class RasaInterface:
    def interact(msg):
        payload = {"sender":"user",
                    "message": msg}
        r = requests.post(f'http://localhost:{PORT}/webhooks/rest/webhook', json=payload)

        metadata = requests.get(f"http://localhost:{PORT}/conversations/default/tracker")
        intents = metadata.json()

        print(intents)

        return r.json()[0]['text'] if r.json() else None
    