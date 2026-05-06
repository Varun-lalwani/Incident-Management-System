from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["ims_db"] 

signals_collection = db["signals"]