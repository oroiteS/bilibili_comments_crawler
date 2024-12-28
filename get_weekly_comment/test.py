import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")  # Host以及port
db = myclient["big_data"]
coll = db['bilibili']
for i in range(84, 99):
    coll.delete_many({'phase': f"{i}"})
