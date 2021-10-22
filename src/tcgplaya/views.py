from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
    listing = CardListing.objects.get(id=id)
    in_cart, seller = 'no', False
    if request.user.username:
        # redirect user to register page if not logged in
        profile = Profile.objects.get(user = request.user)

        # check if cardlisting in cart
        cart = profile.cart.all()
        for cart_listing in cart:
            print(cart_listing)
            if cart_listing.id == id:
                in_cart = 'yes'
                break
        
        # check if user is the seller of the cardlisting
        if profile == listing.seller:
            seller = True
            in_cart = 'seller'

    context = {
        'listing': listing,
        'in_cart': in_cart,
        'seller': seller,
        'user': request.user,
    }

    return render(request, 'tcgplaya/cardlisting.html', context)

@csrf_exempt
def ajax_cart_request(request):
    id = request.POST.get('id')
    listing = CardListing.objects.get(id=id)
    in_cart = 'no'
    if request.user:
        # redirect user to register page if not logged in
        profile = Profile.objects.get(user = request.user)

        # check if cardlisting in cart
        cart = profile.cart.all()
        for cart_listing in cart:
            print(cart_listing)
            if cart_listing.id == id:
                in_cart = 'yes'
                break
        
        # check if user is the seller of the cardlisting
        if profile == listing.seller:
            seller = True
            in_cart = 'seller'
    
    if request.method == "POST":
        if request.user:
            # add and remove from cart, delete listing
            if request.POST.get('add_cart'):
                in_cart = 'yes'
                profile.cart.add(listing)
                # return redirect('/cart/')
            elif request.POST.get('remove_cart'):
                print("removing cardlisting")
                in_cart = 'no'
                profile.cart.remove(listing)
                # return redirect('/cart/')
            elif request.POST.get('delete_listing'):
                print("deleting listing")
                listing.delete()
                return redirect('/cards/cardlistings/')
        else:
            return redirect('/register/')

    context = {
        'in_cart': in_cart,
    }
    print(context)
    return JsonResponse(context)

# create a new cardlisting from a given card
def new_cardlisting_view(request, id):
    if not request.user.username:
        # redirect user to register page if not logged in
        return redirect('/register/')
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

# user's own listings view
def my_listings_view(request):
    if not request.user.username:
        # redirect user to register page if not logged in
        return redirect('/register/')
    profile = Profile.objects.get(user = request.user)
    # get user's saved card listings
    my_listings = []
    listings = CardListing.objects.all()
    for listing in listings:
        if listing.seller == profile:
            my_listings.append(listing)
    context = {
        'listings': my_listings
    }
    return render(request, 'tcgplaya/my_listings.html', context)