from django.urls import path
from .views import NearbyFoodTrucks, AllFoodTrucks, SearchFoodTrucks

urlpatterns = [
    path('nearby/', NearbyFoodTrucks.as_view(),name='nearByFoodTrucks'),
    path('all/', AllFoodTrucks.as_view(),name='allFoodTrucks'),   
    path('search/', SearchFoodTrucks.as_view(),name='searchFoodTrucks'),
]