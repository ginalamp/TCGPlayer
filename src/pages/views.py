# Renders the general html templates
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# profile page
from .forms import CreateUserForm, LoginForm, UpdateProfileForm, UpdateUserForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from tcgplaya.models import Card, Profile
from .forms import CreateUserForm, LoginForm

import pandas as pd

# home page
def home_view(request):
    context = {}
    values = Card.objects \
        .order_by('name') \
        .values('id', 'name', 'img_uri')[4:101]
    df = pd.DataFrame(values)
    # remove all rows with duplicate names
    df = df.drop_duplicates(subset='name', keep='first')
    # export df to list of dicts
    context['cards'] = df.to_dict('records')
    return render(request, 'home.html', context)

# home page search bar
def home_searched(request):
    if request.method == "POST":
        searched = request.POST['searched']
        cards = Card.objects.filter(name__contains = searched)
        if not cards:
            return render(request, 'home_searched.html', {})
        context = {
            'searched': searched,
            'cards': cards
        }
        return render(request, 'home_searched.html', context)
        
    return render(request, 'home_searched.html', {})

# register page
def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            # password = request.POST.get('password')
            print(f"(Registered User: {username}")
            form = CreateUserForm() # makes form blank after saving
            return redirect("/login/")
        else:
            print(form.errors)
            print('invalid register form')
    
    context = {'form': form}
    return render(request, 'register.html', context)

# login page
def login_view(request):
    form = LoginForm()
    form.error_msg = ''
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        context = {'form':form}
        return render(request, 'login.html', context)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/home/")
    else:
        form.error_msg = 'Username and Password do not match.'
        print('Invalid log in username/password details provided')
    
    context = {'form':form}
    return render(request, 'login.html', context)

# cart page
def cart_view(request):
    if not request.user.username:
        # redirect user to register page if not logged in
        return redirect('/register/')
    
    # get user's saved card listings
    profile = Profile.objects.get(user = request.user)
    cart = [ cardlisting for cardlisting in profile.cart.all() ]
    context = {
        'listings': cart
    }
    return render(request, 'cart.html', context)

# profile
def profile_view(request, ):
    print(request.POST.get('showPassChangeToast'))
    if not request.user.username:
        # redirect user to register page if not logged in
        return redirect('/register/')
    else:
        profile_form = UpdateProfileForm()
        print("current user:", request.user)

        if request.method == 'POST':
            if request.POST.get('logout'):
                logout(request)
                return redirect('/login/')

            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                print('User form and profile form valid')
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been successfully updated.')
                return redirect('/profile')
            else:
                print('User form or profile form not valid')
                user_form = UpdateUserForm(instance=request.user)
                profile_form = UpdateProfileForm(instance=request.user.profile)
        
        return render(request, 'profile.html', {'profile_form': profile_form})

# change password
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('pages:profile')