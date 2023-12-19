import requests

PORT = 5005

class RasaInterface:
    def interact(msg):
        r = requests.post(f'http://localhost:{PORT}/webhooks/rest/webhook', json={"message": msg})
        return r.json()[0]['text'] if r.json() else None
    