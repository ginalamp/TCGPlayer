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
    
    # clean dataframe
    df = clean_bulk_df(og_df)
    print(df)



def clean_bulk_df(og_df):
    '''
    Return cleaned dataframe
    @param og_df pre-cleaned dataframe created from Scryfall bulk_data json file
    '''
    # stringify everything
    df = og_df.astype(str)
    # replace nan colors
    df.colors[df.colors == 'nan'] = '[]'
    # set all power/toughness/flavor_text 'nan' to ''
    df.power[df.power == 'nan'] = ''
    df.toughness[df.toughness == 'nan'] = ''
    df.flavor_text[df.flavor_text == 'nan'] = ''
    df.edhrec_rank[df.edhrec_rank == 'nan'] = '-1'
    df.edhrec_rank = df.edhrec_rank.astype(float)
    # collect image uris
    df.image_uris = og_df.image_uris.where(pd.notnull(og_df.image_uris), {})
    # collect prices
    df.prices = og_df.prices.where(pd.notnull(og_df.prices), {})
    # convert released_at to timestamp
    df.released_at = pd.to_datetime(df.released_at)

    return df
