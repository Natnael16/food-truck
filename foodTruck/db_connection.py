from pymongo import MongoClient

# MongoDB connection URL specifying the host and port.
url = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'

# Create a MongoClient instance to connect to the MongoDB server.
db_client = MongoClient(url)

# Select the 'food_truck_finder' database from the connected MongoDB server.
db = db_client['food_truck_finder']

# Create a 2dsphere index on the 'location' field of the 'food_truck' collection.
# This index is used for geo-spatial queries, which allow efficient querying based on geographical proximity.
db['food_truck'].create_index({"location": '2dsphere'})