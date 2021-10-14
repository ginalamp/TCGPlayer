from django.urls import path
from . import views

# pages url configuration
app_name = 'pages'
urlpatterns = [
    path('', views.home_view),
    path('home/', views.home_view),
]