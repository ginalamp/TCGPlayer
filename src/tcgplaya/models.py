from django.db import models

price_kwargs = dict(
    default=0.0, decimal_places=2, max_digits=6,
    blank=True, null=True)

# Card based on some of Scryfall's MTG card fields
class Card(models.Model):
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

