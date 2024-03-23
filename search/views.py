from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FoodTruckSerializer
from django.http import JsonResponse
from foodTruck.db_connection import db
from .utils import validate_location_params

# get food truck collection
food_truck_collection = db['food_truck']

class NearbyFoodTrucks(APIView):
    """
    API endpoint to retrieve nearby food trucks based on provided location coordinates.

    Expected Query Parameters:
        - latitude: Latitude coordinate of the center point for the search (default: 0).
        - longitude: Longitude coordinate of the center point for the search (default: 0).
        - radius: Search radius in meters (default: 1000).

    Returns:
        - JSON response containing count and data of nearby food trucks.
    """
    def get(self, request):
        query_params = request.query_params
        latitude = query_params.get('latitude', 0)
        longitude = query_params.get('longitude', 0)
        radius = query_params.get('radius', 1000)

        is_valid = validate_location_params(latitude, longitude, radius)
        if not is_valid:
            return Response({'error_message': "invalid location filter parameter"}, status=http_status.HTTP_400_BAD_REQUEST)

        location = [float(longitude), float(latitude)]
        query = {
            'location': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': location
                    },
                    '$maxDistance': float(radius)
                }
            }
        }
        nearby_foodtrucks = food_truck_collection.find(query)
        serializer = FoodTruckSerializer(nearby_foodtrucks, many=True)
        return Response({'count': len(serializer.data), 'data': serializer.data})


class AllFoodTrucks(APIView):
    """
    API endpoint to retrieve all food trucks from the database.

    Returns:
        - JSON response containing count and data of all food trucks.
    """
    def get(self, request):
        all_food_trucks = food_truck_collection.find()
        serializer = FoodTruckSerializer(all_food_trucks, many=True)
        return Response({'count': len(serializer.data), 'data': serializer.data})


class SearchFoodTrucks(APIView):
    """
    API endpoint to search for food trucks based on various filters.

    Expected Query Parameters:
        - q: Search query string.
        - status: Filter by status.
        - facility_type: Filter by facility type.
        - latitude: Latitude coordinate for geospatial search.
        - longitude: Longitude coordinate for geospatial search.
        - radius: Search radius in meters for geospatial search.

    Returns:
        - JSON response containing count and data of searched food trucks.
    """
    def get(self, request):
        query_params = request.query_params
        search_query = query_params.get('q', '')
        status = query_params.get('status', None)
        facility_type = query_params.get('facility_type', None)
        latitude = query_params.get('latitude', None)
        longitude = query_params.get('longitude', None)
        radius = query_params.get('radius', None)

        if latitude and longitude:
            is_valid = validate_location_params(latitude, longitude, radius)
            if not is_valid:
                return Response({'error_message': "invalid location filter parameter"}, status=http_status.HTTP_400_BAD_REQUEST)

        pipeline = []
        match_stage = {}

        if search_query:
            match_stage['$or'] = [
                {'applicant': {'$regex': search_query, '$options': 'i'}},
                {'address': {'$regex': search_query, '$options': 'i'}},
                {'food_items': {'$elemMatch': {'$regex': search_query, '$options': 'i'}}}
            ]

        if status:
            match_stage['status'] = status

        if facility_type:
            match_stage['facility_type'] = facility_type

        if latitude and longitude and radius:
            pipeline.append({
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [float(longitude), float(latitude)]
                    },
                    'distanceField': 'distance',
                    'maxDistance': float(radius),
                    'spherical': True
                }
            })

        if match_stage:
            pipeline.append({'$match': match_stage})

        pipeline.append({'$project': {'_id': 0}})
        result = food_truck_collection.aggregate(pipeline)
        result = list(result)
        return JsonResponse({"count": len(result), 'data': result}, safe=False)
