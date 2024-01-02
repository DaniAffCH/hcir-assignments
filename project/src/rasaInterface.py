import requests

PORT = 5005

class RasaInterface:
    def interact(msg):
        payload = {"sender":"user",
                    "message": msg}
        r = requests.post(f'http://localhost:{PORT}/webhooks/rest/webhook', json=payload)

        r = r.json()

        return ". ".join([e["text"] for e in r]) if r else None
    