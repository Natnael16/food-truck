
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FoodTruckSerializer
from django.http import JsonResponse
from foodTruck.db_connection import db


# get food truck collection
food_truck_collection = db['food_truck']

# Create your views here.
class NearbyFoodTrucks(APIView):
    def get(self, request):
        # recieve radius and locaiton [lat, log] from request
        query_params = request.query_params
        location = query_params.get('location', None)  # Location coordinates
        radius = query_params.get('radius', None)
        #! validate query parameters
        # A query that filters food tracks with in <radius> meters from the <location> center
        query = {
        'location': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': location
                    },
                '$maxDistance': radius, 
                'spherical': True
 
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
            return Response(serializer.data)
        
        
class SearchFoodTrucks(APIView):
    def get(self, request):
        # Get parameters from the request
        query_params = request.query_params
        search_query = query_params.get('q', '')  # Search query
        status = query_params.get('status', None)  # Status filter
        facility_type = query_params.get('facility_type', None)  # Facility type filter
        location = query_params.get('location', None)  # Location coordinates
        radius = query_params.get('radius', None)# Radius for geospatial search

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
        
        # if geolocation included it should be a separate dictionary starting with $geoNear separated with a comma
        if location and radius:

            # Geospatial query stage
            longitude, latitude = map(float, reversed(str(location).split(','))) # lat,long format for locaiton
            pipeline.append({
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude]
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

        # Iterate over results and check availability
        # for truck in result:
        #     truck['is_available_now'] = self.check_availability(truck.get('open_hours'))

        return JsonResponse(list(result), safe=False)

    def check_availability(self, open_hours):
        # Implement logic to check availability based on open hours
        # Return True if available, False otherwise
        # Example implementation:
        # current_time = datetime.now().time()
        # Implement your logic to check if current_time falls within any open hours
        pass
 
    
    
    