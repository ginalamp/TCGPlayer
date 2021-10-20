# Renders the general html templates
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tcgplaya.models import Card
from .forms import CreateUserForm, LoginForm

# home page
def home_view(request):
    context = {}
    cards = Card.objects.all()[:16]
    values = cards.values('id', 'name', 'img_uri')
    context['cards'] = values

    return render(request, 'home.html', context)

# register page
def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print(password)
            form = CreateUserForm() # makes form blank after saving
            return redirect("/login/")
        else:
            print('invalid form')
    
    context = {'form':form}
    return render(request, 'register.html', context)

# login page
def login_view(request):
    form = LoginForm()
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        return redirect('/')
    else:
        print('who u')
    
    context = {'form':form}
    return render(request, 'login.html', context)

# cart page
def cart_view(request):
    context = {}
    return render(request, 'cart.html', context)

# profile
def profile_view(request):
    context = {}
    return render(request, 'profile.html', context)