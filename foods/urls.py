from django.urls import path
from .views import SearchFoods

urlpatterns = [
    path('search/', SearchFoods.as_view(),name='searchFoods'),
]