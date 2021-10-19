from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# TODO: update which fields need to be mandatory, etc
# TODO: manytomany Cart - profile can have many cards, and a card can be part of many profiles (get buyer best price - cheapest price for user by querying all cardlistings for that card)

# format price Decimal Fields
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

    # used for getting image url e.g. https://c1.scryfall.com/file/scryfall-cards/normal/front/b/e/be72ff91-f810-46c3-884f-6e65827824bc.jpg?1598917660
    img_uri = models.CharField(default='', max_length=100)

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

    # string representation of self
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

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
    
    # string representation of self
    def __str__(self):
        return self.set_name

    def __repr__(self):
        return str(self)

class CardListing(models.Model):
    '''
    Represents a user selling a card
    '''
    # the card that this listing is for
    card = models.ForeignKey('Card', null=True, default=None,
                             on_delete=models.CASCADE)
    # the user that is selling the card(s)
    seller = models.ForeignKey('Profile', related_name='seller',
                               on_delete=models.CASCADE)
    # the price of the card
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    # the listed quantity of the card being listed
    quantity = models.IntegerField(default=0)
    # the buyer (if null, the card(s) has not been bought yet)
    buyer = models.ForeignKey('Profile', null=True, related_name='buyer', blank=True,
                              on_delete=models.CASCADE)
    
    # string representation of self
    def __str__(self):
        return f'CardListing(card={self.card}, seller={self.seller}, price={self.price})'

    def __repr__(self):
        return str(self)

#######################################################
# USERS
#######################################################

class Profile(models.Model):
    '''
    User profile: extension of django.contrib.auth.model.User
    '''
    # the user this profile is for
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the user's username
    username = models.TextField(default='')
    
    # string representaion of self
    def __str__(self):
        return f'Profile(user={self.user}, email={self.user.email})'
    
    def __repr__(self):
        return str(self)

# if the user is created, a profile is created as well
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
# when the user is saved, their profile is saved as well
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()