# Dealing with the api/data
import requests
import json
import pandas as pd
from tcgplaya.models import *
from tqdm import tqdm

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
    '''
    Add Scryfall's bulk_data to the tcgplaya models.
    @param filename path to the downloaded json Scryfall bulk data file.
    '''
    # delete all data
    print(f"wiping database...")
    Card.objects.all().delete()
    CardSet.objects.all().delete()

    # load bulk data
    print(f"loading file...")
    with open(filename, 'r') as f:
        bulkdata = json.load(f)

    # convert json file to dataframe
    print(f"building dataframe...")
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

    print(f"collecting data...")
    # these keys will be used for the Card
    direct_copy_keys = [
        'card_id', 'name',
        'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'keywords',
        'rarity', 'flavor_text', 'booster', 'edhrec_rank',
    ]
    # these keys will be used for the CardSet
    direct_copy_keys_set = [
        'set_id', 'set_codename', 'set_name', 'set_type'
    ]

    # Add Card data
    cards = []
    set_id2cardset = {}
    cardsets = []
    pbar = tqdm(total=len(df))
    for index, row in df.iterrows():
        # create the cardset obj
        set_kwargs = dict(row[direct_copy_keys_set])
        set_id = set_kwargs['set_id']
        cardset = set_id2cardset.get(set_id)
        if cardset is None:
            cardset = CardSet(**set_kwargs)
            set_id2cardset[set_id] = cardset
        cardsets.append(cardset)

        # get the image id
        img_uri = row.image_uris.get('small')
        if img_uri is None:
            img_id = ''
        else:
            index = img_uri.rfind('?')
            img_id = img_uri[index+1:]
        # set released_at as understandable by Django's DateField
        released_at = row.released_at.date()
        # process the card prices
        prices = dict(row.prices)
        # extract all the keys we can just import directly
        kwargs = dict(row[direct_copy_keys])
        # construct the card
        card = Card(
            img_id=img_id,
            released_at=released_at,
            **prices,
            **kwargs,
        )
        cards.append(card)
        pbar.update(1)
    pbar.close()

    # create card sets
    _cardsets = set_id2cardset.values()
    CardSet.objects.bulk_create(_cardsets)
    # create cards
    Card.objects.bulk_create(cards)

    # Add CardSet data
    print(f"collecting cardsets")
    pbar = tqdm(total=len(df))
    _cardsets = []
    for cardset in cardsets:
        cardset = CardSet.objects.get(set_id=cardset.set_id)
        _cardsets.append(cardset)
        pbar.update(1)
    pbar.close()

    print(f"assigning cardsets to cards")
    pbar = tqdm(total=len(df))
    cards = Card.objects.all().order_by('id')
    for card, cardset in zip(cards, _cardsets):
        card.cardset = cardset
        card.save()
        pbar.update(1)
    pbar.close()
    
    print(f"updating cards...")
    Card.objects.bulk_update(cards, ['cardset'])


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
