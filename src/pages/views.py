# Renders the general html templates
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

#import user creation form that I customised from the django standard UserCreationForm
#customised to add an email field and phone number field - since a seller must provide contact info
from .forms import CreateUserForm

# home page
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

#register page
def register_view(request, *args, **kwargs):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form':form}
    return render(request, "register.html", context)

#login page
def login_view(request, *args, **kwargs):
    return render(request, "login.html", {})


