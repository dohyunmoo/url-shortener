from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
urls_collection = db["urls"]  # Specify the collection name

urls_collection.delete_many({})
