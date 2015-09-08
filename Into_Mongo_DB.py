__author__ = 'thomaswoodside'
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
test = client.drop_database('OSM')
db = client.OSM
map_data_JSON = open("map.json")
for row in map_data_JSON:
    map_data_dict = json.loads(row)
    try:
        db.OSM.insert(map_data_dict)
    except:
        print(map_data_dict)
