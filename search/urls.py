from django.urls import path
from .views import NearbyFoodTrucks, AllFoodTrucks, SearchFoodTrucks

urlpatterns = [
    path('foodtruck/nearby/', NearbyFoodTrucks.as_view(),name='nearByFoodTrucks'),
    path('foodtruck/all/', AllFoodTrucks.as_view(),name='allFoodTrucks'),   
    path('foodtruck/search', SearchFoodTrucks.as_view(),name='searchFoodTrucks'),
]