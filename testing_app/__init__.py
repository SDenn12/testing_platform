from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import Flask

app = Flask(__name__)
app.secret_key = 'super secret key'

client = MongoClient("mongodb://192.168.10.100:27017/my_db")

# try: 
#     client.my_db.command('ping')

# except ConnectionFailure:
#     print("Server not available")

db = client["my_db"]

from testing_app import routes