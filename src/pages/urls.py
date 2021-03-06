from django.urls import path
from . import views
from tcgplaya.views import ajax_cart_request
from pages.views import ChangePasswordView
from django.conf.urls import include, url


# pages url configuration
app_name = 'pages'
urlpatterns = [
    path('', views.home_view, name = ''),
    path('home/', views.home_view, name = 'home'),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('profile/', views.profile_view, name = 'profile'),
    path('cart/', views.cart_view, name = 'cart'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('home_searched/', views.home_searched, name = 'home-searched'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_to_cart', ajax_cart_request)
]
