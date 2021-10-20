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

# create a new cardlisting from a given card
def new_cardlisting_view(request, id):
    context = {}
    print(request)
    if request.method == "POST":
        listing_price = request.POST.get('listing_price')
        print("listing price --->", listing_price)
        # create new cardlisting
        card = Card.objects.get(id=id)
        print(request.user)
        # print(request.user.profile)
        if listing_price is not None:
            cardlisting = CardListing.objects.create(
                card=card,
                seller=request.user,
                price=listing_price
            )
            print("new cardlisting created: ", cardlisting)

        context = {
            'card': card,
            'suggest_price': card.usd,
            'listing_price': listing_price,
        }
    return render(request, 'tcgplaya/new_cardlisting.html', context)