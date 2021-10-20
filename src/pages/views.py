# Renders the general html templates
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# Import user creation form that I customised from the django standard UserCreationForm
# Customised to add an email field and phone number field - since a seller must provide contact info
from .forms import CreateUserForm

# home page
def home_view(request, *args, **kwargs):
    context = {}
    return render(request, 'home.html', context)

# register page
def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = CreateUserForm() # makes form blank after saving
            return redirect("/login/")
    
    context = {'form':form}
    return render(request, 'register.html', context)

# login page
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        # login(request, user)
        # Redirect to a success page.
        return redirect('/')
    else:
        # Return san 'invalid login' error message.
        print('who u')
    
    # profile = user.profile
    # context = {}
    # return render(request, 'login.html', context)
    return render(request, 'login.html', {})

# cart page
def cart_view(request):
    context = {}
    return render(request, 'cart.html', context)

# profile
def profile_view(request):
    context = {}
    return render(request, 'profile.html', context)