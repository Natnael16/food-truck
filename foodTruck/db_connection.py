import pymongo

url = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'

db_client = pymongo.MongoClient(url)

db = db_client['food_truck_finder']
