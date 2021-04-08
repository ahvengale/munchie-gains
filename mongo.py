from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
print(client.server_info())
