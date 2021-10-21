from django.shortcuts import redirect, render
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
    listings = CardListing.objects.all()
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
    print(request.user)
    if request.method == "POST":
        listing_price = request.POST.get('listing_price')
        print("listing price --->", listing_price)
        # create new cardlisting
        card = Card.objects.get(id=id)
        seller_profile = Profile.objects.get(user = request.user)
        print(seller_profile)
        if listing_price is not None:
            cardlisting = CardListing.objects.create(
                card=card,
                seller=seller_profile,
                price=listing_price
            )
            print("new cardlisting created: ", cardlisting)
            return redirect(f'/cards/card/{id}')

        context = {
            'card': card,
            'suggest_price': card.usd,
            'listing_price': listing_price,
        }
    return render(request, 'tcgplaya/new_cardlisting.html', context)

# functional cardlistings page search bar
def cardlistings_searched(request):
    if request.method == "POST":
        searchedL = request.POST['searchedL']
        listings = CardListing.objects.all()
        # listings = CardListing.objects.filter(card__name__icontains = searchedL)

        # if not listings:
        #     return render(request, 'tcgplaya/cardlistings_searched.html', {})
        # context = {
        #     'searched': searchedL,
        #     'listings': listings
        # }
        # get all listings whose cards contain searched word
        matched_search_listings = []
        for listing in listings:
            if searchedL.lower() in listing.card.name.lower():
                matched_search_listings.append(listing)

        # return empty dict if no matches found
        if not matched_search_listings:
            return render(request, 'tcgplaya/cardlistings_searched.html', {})

        context = {
            'searchedL': searchedL,
            'listings': matched_search_listings
        }
        return render(request, 'tcgplaya/cardlistings_searched.html', context)
        
    return render(request, 'tcgplaya/cardlistings_searched.html', {})


# def home_searched(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         cards = Card.objects.filter(name__contains = searched)
#         if not cards:
#             return render(request, 'home_searched.html', {})
#         context = {
#             'searched': searched,
#             'cards': cards
#         }
#         return render(request, 'home_searched.html', context)
        
#     return render(request, 'home_searched.html', {})