import pymongo

url = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'

dbClient = pymongo.MongoClient(url)

db = dbClient['food_truck_finder']
