"""
Paths:
------
GET /suppliers - Returns a list all of the suppliers
GET /suppliers/{id} - Returns the supplier with a given id number
POST /suppliers - creates a new supplier record in the database
PUT /suppliers/{id} - updates a supplier record in the database
DELETE /suppliers/{id} - deletes a supplier record in the database
QUERY
ACTION
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from service.models import Supplier, DataValidationError

from . import app


# server = Flask(__name__)
# server.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(server)

# PyMongo connects to the MongoDB server running on port 27017 on localhost,
# to the database named myDatabase.
# This database is exposed as the db attribute. (mongo.db)
######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR



@app.route('/suppliers/<int:supplierID>', methods = ['GET'])
def read(supplierID):
	return str(supplierID)

######################################################################
# ADD A NEW SUPPLIER
######################################################################

@app.route('/suppliers', methods = ['POST'])
def create_suppliers():
    """
    Creates a Supplier
    This endpoint will create a Supplier based the data in the body that is posted
    """
    # app.logger.info('Request to create a supplier')
    check_content_type('application/json')
    supplier = Supplier()
    data = request.get_json()
    # supplier.deserialize(data)
    # supplier.save()
    # message = supplier.serialize()
    # location_url = url_for('get_suppliers', supplier_id=supplier.supplierID, _external=True)
    # return make_response(jsonify(message), status.HTTP_201_CREATED,
    #                     {
    #                         'Location': location_url
    #                     })
    return "123"

@app.route('/')
def index():
    return "Welcome to supplier team!"

@app.route('/suppliers', methods = ['GET'])
def list_suppliers():
    return "list of suppliers"

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the mongoengine """
    global app
    Supplier.init_db(app)

# if __name__ == '__main__':
#     app.run()
