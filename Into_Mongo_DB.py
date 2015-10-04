__author__ = 'thomaswoodside'
from pymongo import MongoClient
import json

#loads the data into MongoDB
client = MongoClient('mongodb://localhost:27017/')
test = client.drop_database('OSM')
db = client.OSM
map_data_JSON = open("map.json")
num = 0
for row in map_data_JSON:
    try:
        map_data_dict = json.loads(row)
    except:
        print("Error.")
    num+=1
    try:
        db.OSM.insert(map_data_dict)
    except:
        print(map_data_dict)
        print(num)
