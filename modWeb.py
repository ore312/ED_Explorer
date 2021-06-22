import requests
import json

def getApi(pUri):
    aRef = requests.get(pUri)
    if aRef.status_code != 200:
        return None
    return json.loads(aRef.text)
