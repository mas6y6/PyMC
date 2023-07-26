import requests
import json
import ast


def check_for_updates():
    data = requests.get("https://api.github.com/repos/mas6y6/PyMC-Server/releases")
    returndata = list(json.loads(data.text))
    return returndata[len(returndata) - 1]["tag_name"]

print(check_for_updates())