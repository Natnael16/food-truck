from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import FoodTruck

class FoodTruckSerializer(DocumentSerializer):
    class Meta:
        model = FoodTruck
        fields = '__all__'  