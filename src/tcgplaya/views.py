from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from django.contrib.auth.models import User

# single card view
def card_view(request, id):
    context = {}
    card = Card.objects.get(id=id)
    listings = CardListing.objects.filter(card=card)
    listings = listings.order_by('price')

    context = dict(
        card = card,
        listings=listings
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