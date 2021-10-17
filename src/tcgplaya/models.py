from django.db import models

price_kwargs = dict(
    default=0.0, decimal_places=2, max_digits=6,
    blank=True, null=True)

class Card(models.Model):
    '''
    Card based on some of Scryfall's MTG card fields.
    '''
    # e.g. '0000579f-7b35-4ed3-b44c-db2a538066fe'
    card_id = models.CharField(default='', max_length=36)
    name = models.CharField(default='', max_length=256)
    # this card's set
    cardset = models.ForeignKey('CardSet', null=True, default=None,
                                on_delete=models.CASCADE)

    # e.g. 'uncommon', 'common', 'rare', 'mythic', 'special', 'bonus'
    rarity = models.CharField(default='', max_length=8)

    # the prices available for this card
    usd = models.DecimalField(**price_kwargs)
    usd_foil = models.DecimalField(**price_kwargs)
    usd_etched = models.DecimalField(**price_kwargs)
    eur = models.DecimalField(**price_kwargs)
    eur_foil = models.DecimalField(**price_kwargs)
    tix = models.DecimalField(**price_kwargs)

    released_at = models.DateField(blank=True, null=True)
    # used for getting image e.g. '1562894979'
    img_id = models.CharField(default='', max_length=10)

    # e.g. '{X}{W} // {2}{R} // {2}{U} // {3}{B} // {1}{G}', '{5}{R}'
    mana_cost = models.CharField(default='', max_length=46)
    # e.g. 6.0, max: 1000000.0
    cmc = models.DecimalField(default=0, decimal_places=1, max_digits=8,
                              blank=True, null=True)
    # e.g. 'Creature — Siren Pirate'
    type_line = models.CharField(default='', max_length=80)
    # ability of the card. max len is 769
    oracle_text = models.CharField(default='', max_length=800)
    
    # e.g. '3', '', '*', '-1', '1+*', '?', '.5'
    power = models.CharField(default='', max_length=3)
    toughness = models.CharField(default='', max_length=3)
    # e.g. "['B', 'R']", max len: "['B', 'G', 'R', 'U', 'W']"
    colors = models.CharField(default='', max_length=25)
    # e.g. ['Landwalk', 'Flanking', 'Fading'], maxlen: 124
    keywords = models.CharField(default='', max_length=128)

    # adds character to the card, usually a moto or a tagline. max: 448
    flavor_text = models.CharField(default='', max_length=500)
    # whether or not this card was part of a booster or not
    booster = models.BooleanField(default=False)
    # some rank (not always available)
    edhrec_rank = models.DecimalField(default=0, decimal_places=1, max_digits=8,
                                      blank=True, null=True)

class CardSet(models.Model):
    '''
    Cards can be part of a card set
    '''
    # e.g. 'c1d109bc-ffd8-428f-8d7d-3f8d7e648046'
    set_id = models.CharField(default='', max_length=256)
    # e.g. 'tsp'
    set_codename = models.CharField(default='', max_length=256)
    # e.g. 'Time Spiral'
    set_name = models.CharField(default='', max_length=256)
    # e.g. expansion, core, token
    set_type = models.CharField(default='', max_length=256)