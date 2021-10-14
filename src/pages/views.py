# Renders the general html templates
from django.shortcuts import render
from django.http import HttpResponse

# home page
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})
