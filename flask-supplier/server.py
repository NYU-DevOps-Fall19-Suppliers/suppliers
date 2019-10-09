from flask import Flask
from flask_pymongo import PyMongo




server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(server)

# PyMongo connects to the MongoDB server running on port 27017 on localhost,
# to the database named myDatabase.
# This database is exposed as the db attribute. (mongo.db)

@server.route('/suppliers/<int:supplierID>', methods = ['GET'])
def read(supplierID):
	return str(supplierID)

@server.route('/')
def index():
    return "Welcome to supplier team!"

if __name__ == '__main__':
    server.run()
