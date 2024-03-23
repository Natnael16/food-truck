from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FoodTruckSerializer
from django.http import JsonResponse
from foodTruck.db_connection import db
from .utils import validate_location_params

# get food truck collection
food_truck_collection = db['food_truck']

# Create your views here.
class NearbyFoodTrucks(APIView):
    def get(self, request):
        query_params = request.query_params
        latitude = query_params.get('latitude', 0)  # Assuming latitude is provided as a float
        longitude = query_params.get('longitude', 0)
        radius = query_params.get('radius', 1000)

        is_valid = validate_location_params(latitude,longitude,radius)
        if not is_valid:
            return Response({'error_message': "invalid location filter parameter",}, status=http_status.HTTP_400_BAD_REQUEST)
        location = [float(longitude), float(latitude)]      

        # A query that filters food tracks with in <radius> meters from the <location> center
        query = {
        'location': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': location
                    },
                '$maxDistance': float(radius), 
 
                }
            }
        }
        nearby_foodtrucks = food_truck_collection.find(query)
        serializer = FoodTruckSerializer(nearby_foodtrucks, many=True)
        return Response({'count': len(serializer.data),'data': serializer.data, })
    
    
class AllFoodTrucks(APIView):
    def get(self, request):
            # fetch all food trucks from database
            all_food_trucks = food_truck_collection.find()
            serializer = FoodTruckSerializer(all_food_trucks, many=True)
            return Response({'count': len(serializer.data), 'data': serializer.data})
        
        
class SearchFoodTrucks(APIView):
    def get(self, request):
        # Get parameters from the request
        query_params = request.query_params
        search_query = query_params.get('q', '')  # Search query
        status = query_params.get('status', None)  # Status filter
        facility_type = query_params.get('facility_type', None)  # Facility type filter
        latitude = query_params.get('latitude', None)  # latitude coordinate
        longitude = query_params.get('longitude', None)  # longitude coordinate
        radius = query_params.get('radius', None)# Radius for geospatial search
        
        if latitude and longitude:
            is_valid = validate_location_params(latitude,longitude,radius)
            if not is_valid:
                return Response({'error_message': "invalid location filter parameter"},status=http_status.HTTP_400_BAD_REQUEST)
        

        # MongoDB connection
        pipeline = []

        # Match stage for filtering
        match_stage = {}
        if search_query:
            match_stage['$or'] = [
                {'applicant': {'$regex': search_query, '$options': 'i'}}, # search applicant field. case-insensitive. 
                {'address': {'$regex': search_query, '$options': 'i'}}, # search address field. case-insensitive
                {'food_items': {'$elemMatch': {'$regex': search_query, '$options': 'i'}}}

                
            ]
        # if status included on the query include on search
        if status:
            match_stage['status'] = status 
            
        # if facility_type included on the query include on search
        if facility_type:
            match_stage['facility_type'] = facility_type
        
        if latitude and longitude and radius:

            # Geospatial query stage
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

        # Projection stage and exclude _id field
        pipeline.append({'$project': {'_id': 0}})

        # Execute the aggregation pipeline
        result = food_truck_collection.aggregate(pipeline)

        
        result = list(result)
        return JsonResponse({"count" :len(result),  'data':result }, safe=False)

 
    
    
    