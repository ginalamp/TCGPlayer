from django.urls import path
from . import views

# tcgplaya url configuration
app_name = 'tcgplaya'
urlpatterns = [
    path('card/<int:id>', views.card_view),
    path('cardlistings/', views.cardlistings_view),
    path('cardlisting/<int:id>', views.cardlisting_view),
    path('new-cardlisting/<int:id>', views.new_cardlisting_view),    
    path('cardlistings_searched/', views.cardlistings_searched)
    
    
]