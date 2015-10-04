__author__ = 'thomaswoodside'
from pymongo import MongoClient

#Runs various aggregate functions used in the final report.

client = MongoClient(connect=False)
db = client.OSM

shops = db.OSM.aggregate([
    {'$match': {'shop': {'$exists': True}}},
    {'$group': {'_id': '$shop', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}},
    {'$limit' : 5}
])

numshops = db.OSM.aggregate([
    {'$match': {'shop': {'$exists': True}}},
    {'$group': {'_id': 'null', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
])

postcodes = db.OSM.aggregate([
    {'$match': {'shop': {'$exists': True}}},
    {'$group': {'_id': 'null', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
])

leisure = db.OSM.aggregate([
    {'$match': {'leisure': {'$exists': True}}},
    {'$group': {'_id': '$leisure', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}},
    {'$limit': 3}
])

unique_users = db.OSM.aggregate([
    {'$group': {'_id': '$created.user'}},
    {'$group': {'_id': 'null', 'count': {'$sum': 1}}}
])

nodesways = db.OSM.aggregate([
    {'$match': {'type': {'$exists': True}}},
    {'$group': {'_id': '$type', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
])


for a in nodesways:
    print(a)
