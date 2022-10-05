from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'super secret key'
db_ip = os.environ['DB_HOST']

client = MongoClient(f"mongodb://{db_ip}:27017/my_db")

db = client["my_db"]

from testing_app import routes