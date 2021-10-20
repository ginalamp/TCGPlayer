from django.urls import path
from . import views

# pages url configuration
app_name = 'pages'
urlpatterns = [
    path('', views.home_view),
    path('home/', views.home_view),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('profile/', views.profile_view, name = 'profile'),
    path('cart/', views.cart_view, name = 'cart'),
    path('home_searched/', views.home_searched, name = 'home-searched'),
]