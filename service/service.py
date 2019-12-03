"""
Paths:
------
GET /suppliers - Returns a list all of the suppliers
GET /suppliers/{id} - Returns the supplier with a given id number
POST /suppliers - creates a new supplier record in the database
PUT /suppliers/{id} - updates a supplier record in the database
DELETE /suppliers/{id} - deletes a supplier record in the database
GET /suppliers?averageRating={averageRating} - queries a list of suppliers with given average rating
ACTION /suppliers/{product_id}/recommend - recommends all suppliers that sells given product and has high ratings
"""

import sys
import uuid
import logging
from functools import wraps
import json
from flask import jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flask_restplus import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound
from service.models import Supplier, DataValidationError

from . import app

# server = Flask(__name__)
# server.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

# MongoEngine connects to the MongoDB server running on port 27017 on localhost,
# to the database named myDatabase.
# This database is exposed as the db attribute. (mongo.db)

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Supplier Demo REST API Service',
          description='This is a sample server Supplier server.',
          default='suppliers',
          default_label='Suppliers operations',
          doc='/', # default also could use doc='/apidocs/'
          authorizations=authorizations
          # prefix='/api'
         )

# Define the model so that the docs reflect what can be sent
# id_fields = {}
# id_fields['$oid'] = fields.String(readOnly=True)
supplier_model = api.model('Supplier', {
    'id': fields.String(title = 'supplierId',
                         description='The unique id assigned internally by service'),
    'supplierName': fields.String(required=True,
                          description='The name of the Supplier'),
    'address': fields.String(required=False,
                              description='The address of the Supplier'),
    'productIdList': fields.List(fields.String, required=False,
                                description='The product list of the Supplier'),
    'averageRating': fields.Integer(required = False,
                                description='The average rating of the Supplier')
})

create_model = api.model('supplier', {
    'supplierName': fields.String(required=True,
                          description='The name of the Supplier'),
    'address': fields.String(required=False,
                              description='The address of the Supplier'),
    'productIdList': fields.List(fields.String, required=False,
                                description='The product list of the Supplier'),
    'averageRating' : fields.Integer(required = False,
                                description='The average rating of the Supplier')
})

# query string arguments
supplier_args = reqparse.RequestParser()
# supplier_args.add_argument('supplierName', type=str, required=False, help='List Suppliers by name')
# supplier_args.add_argument('address', type=str, required=False, help='List Suppliers by address')
supplier_args.add_argument('averageRating', type=int, required=False, help='List Suppliers by rating score')
supplier_args.add_argument('rating', type=int, required=False, help='List Suppliers by rating score')

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
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401
    return decorated

######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
#  PATH: /suppliers/{id}
######################################################################
@api.route('/suppliers/<supplier_id>')
@api.param('supplier_id', 'The Supplier Identifier')
class SupplierResource(Resource):
    """
    SupplierResource class

    Allows the manipulation of a single Supplier
    GET /suppliers/{id} - Returns a Supplier with the id
    PUT /suppliers/{id} - Update a Supplier with the id
    DELETE /suppliers/{id} -  Deletes a Supplier with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A SUPPLIER
    #------------------------------------------------------------------ 

    @api.doc('get_suppliers')
    @api.response(404, 'Supplier Not Found')
    @api.marshal_with(supplier_model)
    def get(self, supplier_id):
        """
        Retrieve a single Supplier

        This endpoint will return a Supplier based on it's id
        """ 
        app.logger.info("Request to Retrieve a Supplier with id [%s]", supplier_id)   
        supplier = Supplier.find(supplier_id)
        if not supplier:
            api.abort(status.HTTP_404_NOT_FOUND, "Supplier with id '{}' was not found.".format(supplier_id))   
        return supplier, status.HTTP_200_OK 


######################################################################
#  PATH: /suppliers
######################################################################

######################################################################
# GET A SUPPLIER
######################################################################

@app.route('/suppliers/<string:supplierID>', methods=['GET'])
def get_a_supplier(supplierID):
    """Gets a single supplier
    This endpoint will get a Supplier based on a given supplierID
    """
    supplier = Supplier.find(supplierID)

    if supplier is not None:
        return make_response(supplier.to_json(), status.HTTP_200_OK)
    return not_found("Not Found")

######################################################################
# DELETE A SUPPLIER
######################################################################


@app.route('/suppliers/<string:supplierID>', methods=['DELETE'])
def delete_a_supplier(supplierID):
    """ Route to delete a supplier """
    supplier = Supplier.find(supplierID)
    if supplier:
        supplier.delete()
    return make_response('DELETED', status.HTTP_204_NO_CONTENT)

######################################################################
# ADD A NEW SUPPLIER
######################################################################


@app.route('/suppliers', methods=['POST'])
def create_suppliers():
    """
    Creates a Supplier
    This endpoint will create a Supplier based the data in the body that is posted
    """
    app.logger.info('Request to create a supplier')
    check_content_type('application/json')
    data = request.get_json()
    if not isinstance(data,dict):
        data = json.loads(data)

    try:
        data['supplierName']
    except KeyError as error:
        raise DataValidationError('Invalid supplier: missing ' + error.args[0])
    except TypeError as error:
        raise DataValidationError('Invalid supplier: body of request contained'
                                  'bad or no data')
    supplier = Supplier(**data)
    supplier.save()

    #location_url = url_for('get_suppliers', supplierID=supplier.id, _external=True)
    return make_response(supplier.to_json(), status.HTTP_201_CREATED,
        {'Location': url_for('get_a_supplier', supplierID=supplier.id, _external=True)})


@app.route('/')
def index():
    """index"""
    return app.send_static_file('index.html')
    # return make_response(
    #     jsonify(
    #         name='Supplier Demo REST API Service',
    #         version='1.0',
    #         paths=url_for(
    #             'list_suppliers',
    #             _external=True)),
    #     status.HTTP_200_OK)


@app.route('/suppliers', methods=['GET'])
def list_suppliers():
    """ Route to list all suppliers 
    Args:
        rating: returns all the suppliers with average rating higher than rating.
        averageRating: returns all the suppliers with average rating equaling to averageRating. 
    """
    app.logger.info('Request for supplier list')
    rating = request.args.get('rating')
    averageRating = request.args.get('averageRating')
    if rating:
        suppliers = Supplier.find_by_rating(rating)
        if(len(suppliers) == 0):
            return bad_request("Bad Request")
    elif averageRating:
        suppliers = Supplier.find_by_equals_to_rating(averageRating)
        if(len(suppliers) == 0):
            return bad_request("Bad Request")
    else:
        suppliers = Supplier.all()
    return make_response(suppliers.to_json(), status.HTTP_200_OK)


@app.route('/suppliers/<string:productId>/recommend', methods=['GET'])
def action_recommend_product(productId):
    """ Route to recommend a list of suppliers given a product"""
    app.logger.info('Recommend product')
    suppliers = Supplier.action_make_recommendation(productId)
    if len(suppliers) > 0:
        return make_response(suppliers.to_json(), status.HTTP_200_OK)
    return not_found("Not Found")

######################################################################
# UPDATE AN EXISTING SUPPLIER
######################################################################
@app.route('/suppliers/<string:supplier_id>', methods=['PUT'])
def update_a_supplier(supplier_id):
    """ Update a supplier. """
    app.logger.info('Request to update a supplier')
    check_content_type('application/json')
    data = request.get_json()
    supplier = Supplier.find(supplier_id)
    if not supplier:
        raise NotFound(
            "Supplier with id '{}' was not found.".format(supplier_id))
    supplier.update(**data)
    # supplier.reload()
    supplier = Supplier.find(supplier.id)
    return make_response(supplier.to_json(), status.HTTP_200_OK)

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
        app.logger.error(
            'Invalid Content-Type: %s',
            request.headers['Content-Type'])
        abort(415, 'Content-Type must be {}'.format(content_type))

# if __name__ == '__main__':
#     app.run()
