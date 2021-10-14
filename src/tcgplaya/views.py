from django.shortcuts import render
from django.http import HttpResponse

# cardlisting page (1 card to sell details page)
def cardlisting_view(request, *args, **kwargs):
    return render(request, "tcgplaya/cardlisting.html", {})