from rest_framework.response import Response
from rest_framework.views import APIView
from foodTruck.db_connection import db
from .serializers import FoodSerializer

# Get the MongoDB food collection
food_collection = db['food']

class SearchFoods(APIView):
    """
    API endpoint to search for foods.

    Accepts query parameters for filtering by name.
    """

    def get(self, request):
        """
        Handles GET requests to search for foods.

        Retrieves foods from the database based on the provided query parameters.

        Query Parameters:
            name (str): The name of the food to search for.

        Returns:
            Response: JSON response containing the count of foods and the serialized data.
        """
        query = {}
        name = request.query_params.get('name', None)
        if name:
            # Add name filter to the query using regex for case-insensitive search
            query["name"] = {"$regex": name, "$options": "i"}

        # Find foods matching the query
        foods = food_collection.find(query)
        # Serialize the found foods
        serializer = FoodSerializer(foods, many=True)
        # Return response with count and serialized data
        return Response({"count": len(serializer.data), "data": serializer.data})
