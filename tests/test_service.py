"""
Pet API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import Supplier, DataValidationError #, db
from .suppliers_factory import SupplierFactory
from service.service import app, init_db#, initialize_logging
from mongoengine import connect
from mongoengine.connection import disconnect
# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
# DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestSupplierServer(unittest.TestCase):
    """ Supplier Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        # initialize_logging(logging.INFO)
        # Set up the test database
        # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        disconnect('default')
        db = connect('mydatabase')
        db.drop_database('mydatabase')
        self.app = app.test_client()

    def tearDown(self):
        disconnect('mydatabase')

    def _create_suppliers(self, count):
        """ Factory method to create suppliers in bulk """
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post('/suppliers',
                                 json=test_supplier.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test pet')
            new_supplier = resp.get_json()
            test_supplier.supplierID = new_supplier['supplierID']
            suppliers.append(test_supplier)
        return suppliers
        pass

    def test_index(self):
        """ Test the Home Page """
        # resp = self.app.get('/')
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = resp.get_json()
        # self.assertEqual(data['SupplierName'], 'Pet Demo REST API Service')
        # pass

    def test_create_supplier(self):
        # """ Create a new supplier """
        # test_supplier = SupplierFactory()
        # resp = self.app.post('/suppliers',
        #                      json=test_supplier.serialize(),
        #                      content_type='application/json')
        # # self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # # Make sure location header is set
        # location = resp.headers.get('Location', None)
        # self.assertTrue(location != None)
        # # Check the data is correct
        # new_supplier = resp.get_json()
        # self.assertEqual(new_supplier['supplierName'], test_supplier.supplierName, "SupplierNames do not match")
        # self.assertEqual(new_supplier['address'], test_supplier.address, "Addresses do not match")
        # self.assertEqual(new_supplier['averageRating'], test_supplier.averageRating, "AverageRatings does not match")
        # # Check that the location header was correct
        # resp = self.app.get(location,
        #                     content_type='application/json')
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_supplier = resp.get_json()
        # self.assertEqual(new_supplier['supplierName'], test_supplier.supplierName, "SupplierNames do not match")
        # self.assertEqual(new_supplier['address'], test_supplier.address, "Address do not match")
        # self.assertEqual(new_supplier['averageRating'], test_supplier.averageRating, "AverageRating does not match")
        pass

    def test_update_supplier(self):
        """ Update an existing supplier """
        pass

    def test_get_supplier_list(self):
        """ Get a list of suppliers """
        pass

    def test_get_supplier(self):
        """ Get a single supplier """
        pass

    def test_get_supplier_not_found(self):
        """ Get a Pet thats not found """
        pass


    def test_delete_supplier(self):
        """ Delete a Pet """
        pass

    def test_query_supplier_list_by_rating(self):
        """ Query Pets by Category """
        pass

    # @patch('service.models.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
