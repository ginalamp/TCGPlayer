from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from django.contrib.auth.models import User

# example home view - TODO: move to pages
def home_view(request):
    context = {}
    cards = Card.objects.all()[:9]
    values = cards.values('id', 'name')
    context['cards'] = values

    return render(request, 'tcgplaya/home.html', context)

# single card view
def card_view(request, id):
    context = {}
    card = Card.objects.get(id=id)

    context = dict(
        card = card

        # name=card.name,
        # id=card.id,
        # rarity=card.rarity,
        # card_set=card.cardset,
        # suggested_price=card.usd,
        # card_image=card.img_id,
        # mana_cost=card.mana_cost,
        # power=card.power,
        # toughness=card.toughness,
        # description=card.flavor_text,
        # popularity=card.edhrec_rank
    )
    return render(request, 'tcgplaya/card.html', context)

# multiple cardlistings page
def cardlistings_view(request):
    context = {}
    listings = CardListing.objects.all()[:9]
    # values = listings.values('id', 'name')
    context = dict(
        listings=listings
    )
    # context['listings'] = listings

    return render(request, 'tcgplaya/cardlistings.html', context)

# a single cardlisting for a card
def cardlisting_view(request, id):
    context = {}
    listing = CardListing.objects.get(id=id)
    # values = listings.values('id', 'name')
    context = dict(
        listing=listing
    )
    # context['listings'] = listings

    return render(request, 'tcgplaya/cardlisting.html', context)