# Dealing with the api/data
import requests
import json

# print out hardcoded request to the search API
def api_basic_call():
    parameters = {"q": "Bog Wraith", "pretty": True}
    cards = requests.get("https://api.scryfall.com/cards/search", params=parameters)
    jprint(cards.json())


# print json object as formatted string
def jprint(obj):
   # create a formatted string of the Python JSON object
   text = json.dumps(obj, sort_keys=True, indent=4)
   print(text)
