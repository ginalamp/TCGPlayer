from django.urls import path
from . import views

# tcgplaya url configuration
app_name = 'tcgplaya'
urlpatterns = [
    path('card/<int:id>', views.card_view),
    path('cardlistings/', views.cardlistings_view),
    path('cardlisting/<int:id>', views.cardlisting_view),
    
]