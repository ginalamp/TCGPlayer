# Dealing with the api/data
import requests
import json
import pandas as pd
from tcgplaya.models import *

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

def parse_bulk_data(filename):
    # load bulk data
    with open(filename, 'r') as f:
        bulkdata = json.load(f)

    # convert json file to dataframe
    df = pd.DataFrame(bulkdata)

    # keep only specific columns
    keep = [
        'id', 'name', 'released_at',
        'image_uris',
        'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'keywords',
        'set_id', 'set', 'set_name', 'set_type',
        'rarity', 'flavor_text', 'booster', 'edhrec_rank',
        'prices',
    ]

    # rename columns to match model
    og_df = df[keep].rename(columns={'id': 'card_id', 'set': 'set_codename'})
    print(og_df)
