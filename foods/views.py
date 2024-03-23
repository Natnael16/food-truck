from rest_framework.response import Response
from rest_framework.views import APIView
from foodTruck.db_connection import db
from .serializers import FoodSerializer

food_collection = db['food']

class SearchFoods(APIView):
    def get(self, request):
        query = {}
        name = request.query_params.get('name',None)
        if name:
            query["name"] = {"$regex": name, "$options": "i"}

        foods = food_collection.find(query)
        serializer = FoodSerializer(foods,many=True)
        return Response({"count":len(serializer.data) , "data" : serializer.data})
    