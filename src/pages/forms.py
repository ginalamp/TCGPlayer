from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from tcgplaya.models import Profile

# sign-up form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

# login form
class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        error_msg = ''

# user update form
class UpdateUserForm(forms.ModelForm):
    # username = forms.CharField(max_length=100,
    #                             required=True,
    #                             widget=forms.TextInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(required=True,
    #                             widget = forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','email']

# form for users to edit their profile
class UpdateProfileForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Profile
        fields = ['username', 'email']
