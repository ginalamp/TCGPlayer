from django.urls import path
from . import views

# tcgplaya url configuration
app_name = 'tcgplaya'
urlpatterns = [
    path('', views.cardlisting_view),
]