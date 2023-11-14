from datetime import datetime
import requests

ENDPOINT = "https://openmensa.org/api/v2"
MENSA_ID = 24


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
        print(outStr)




