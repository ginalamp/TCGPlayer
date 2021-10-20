from django.urls import path
from . import views
from pages.views import ChangePasswordView

# pages url configuration
app_name = 'pages'
urlpatterns = [
    path('', views.home_view),
    path('home/', views.home_view),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('profile/', views.profile_view, name = 'profile'),
    path('cart/', views.cart_view, name = 'cart'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password')

]