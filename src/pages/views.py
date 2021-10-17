# Renders the general html templates
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Import user creation form that I customised from the django standard UserCreationForm
# Customised to add an email field and phone number field - since a seller must provide contact info
from .forms import CreateUserForm

# home page
def home_view(request):
    return render(request, "home.html", {})

# register page
def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    
    context = {'form':form}
    return render(request, 'register.html', context)

# login page
def login_view(request):
    context = {}
    return render(request, 'login.html', context)


