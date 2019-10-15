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

# MongoEngine connects to the MongoDB server running on port 27017 on localhost,
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


######################################################################
# GET A SUPPLIER
######################################################################

@app.route('/suppliers/<string:supplierID>', methods = ['GET'])
def read(supplierID):
    supplier = Supplier.find(supplierID)
    return make_response(supplier.to_json(), status.HTTP_201_CREATED)

######################################################################
# ADD A NEW SUPPLIER
######################################################################

@app.route('/suppliers', methods = ['POST'])
def create_suppliers():
    """
    Creates a Supplier
    This endpoint will create a Supplier based the data in the body that is posted
    """
    app.logger.info('Request to create a supplier')
    check_content_type('application/json')
    data = request.get_json()
    try:
        data['supplierName']
    except KeyError as error:
        raise DataValidationError('Invalid supplier: missing ' + error.args[0])
    except TypeError as error:
        raise DataValidationError('Invalid supplier: body of request contained' \
                                  'bad or no data')
    supplier = Supplier(**data)
    supplier.save()
    location_url = url_for('get_suppliers', supplierID=supplier.id, _external=True)
    return make_response(supplier.to_json(), status.HTTP_201_CREATED, {'location': location_url})

@app.route('/')
def index():
    return make_response(jsonify(name = 'Supplier Demo REST API Service',
    version = '1.0', paths = url_for('list_suppliers', _external=True)),
    status.HTTP_200_OK)

@app.route('/suppliers', methods = ['GET'])
def list_suppliers():
    app.logger.info('Request for supplier list')
    suppliers = Supplier.all()
    return make_response(suppliers.to_json(), status.HTTP_200_OK)

@app.route('/suppliers/<string:productId>/recommend', methods = ['GET'])
def action_recommend_product(productId):
    return "A list of the best supplier(rating > 3.5) that supplies the product"

######################################################################
# UPDATE AN EXISTING SUPPLIER
######################################################################
@app.route('/suppliers/<string:supplier_id>', methods=['PUT'])
def update_a_supplier(supplier_id):
    app.logger.info('Request to update a supplier')
    check_content_type('application/json')
    data = request.get_json()
    supplier = Supplier.find(supplier_id)
    supplier.update(**data)
    supplier.reload()
    if not supplier:
        raise NotFound("Supplier with id '{}' was not found.".format(supplier_id))
    return make_response(supplier.to_json(), status.HTTP_201_CREATED)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the mongoengine """
    global app
    Supplier.init_db(app)

def check_content_type(content_type):
    """ Checks whether the request content type is correct """
    if request.headers['Content-Type'] != content_type:
        app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
        abort(415, 'Content-Type must be {}'.format(content_type))

# if __name__ == '__main__':
#     app.run()
