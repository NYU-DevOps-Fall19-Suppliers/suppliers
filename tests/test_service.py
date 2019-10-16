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
import json
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
        db = connect('testdb')
        db.drop_database('testdb')
        self.app = app.test_client()

    def tearDown(self):
        disconnect('testdb')

    def _create_suppliers(self, count):
        """ Factory method to create suppliers in bulk """
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post('/suppliers',
                                 json=test_supplier.to_json(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test supplier')

            new_supplier = json.loads(resp.data)
            test_supplier.id = new_supplier["_id"]["$oid"]
            suppliers.append(test_supplier)
        return suppliers

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Supplier Demo REST API Service')

    def test_create_supplier(self):
        """ Create a new supplier """
        test_supplier = Supplier()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json')
        self.assertRaises(DataValidationError)

        test_supplier = SupplierFactory()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        #self.assertTrue(location != None)
        # Check the data is correct
        new_supplier = json.loads(resp.data)
        self.assertNotEqual(new_supplier, None)
        self.assertNotEqual(test_supplier, None)
        self.assertEqual(new_supplier['supplierName'], test_supplier.supplierName, "SupplierNames do not match")
        self.assertEqual(new_supplier['address'], test_supplier.address, "Addresses do not match")
        self.assertEqual(new_supplier['averageRating'], test_supplier.averageRating, "AverageRatings does not match")
        # Check that the location header was correct
        # resp = self.app.get(location,
        #                     content_type='application/json')
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_supplier = resp.get_json()
        # self.assertEqual(new_supplier['supplierName'], test_supplier.supplierName, "SupplierNames do not match")
        # self.assertEqual(new_supplier['address'], test_supplier.address, "Address do not match")
        # self.assertEqual(new_supplier['averageRating'], test_supplier.averageRating, "AverageRating does not match")

    def test_update_supplier(self):
        """ Update an existing supplier """
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = json.loads(resp.data)
        new_supplier_id = new_supplier["_id"]["$oid"]
        new_supplier.pop('_id', None)
        new_supplier['address'] = 'unknown'
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_supplier = json.loads(resp.data)
        self.assertEqual(updated_supplier['address'], 'unknown')


        new_supplier_id = 0
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                        json=new_supplier,
                        content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)




    def test_get_supplier_list(self):
        """ Get a list of suppliers """
        self._create_suppliers(2)
        resp = self.app.get('/suppliers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_delete_supplier(self):
        """ Delete a Supplier """
        test_supplier = self._create_suppliers(2)[0]
        resp = self.app.delete('/suppliers/{}'.format(test_supplier.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/suppliers/{}'.format(test_supplier.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_supplier(self):
        """ Get a single supplier """

        supplier = self._create_suppliers(1)
        supplier = supplier[0]
        valid_id = supplier.id

        resp = self.app.get('/suppliers/' + valid_id)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        pass

    def test_get_supplier_not_found(self):
        """ Get a supplier thats not found """
        resp = self.app.get('/suppliers/4f4381f4e779897a2c000009')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        pass

    def test_query_supplier_list_by_rating(self):
        """ Query suppliers by rating """
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = json.loads(resp.data)
        new_supplier_id = new_supplier["_id"]["$oid"]
        new_supplier.pop('_id', None)
        new_supplier['supplierName'] = 'Wholefoods'
        new_supplier['address'] = 'unknown'
        new_supplier['averageRating'] = 6
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        resp = self.app.get("/suppliers?rating=6")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        queried_suppliers = json.loads(resp.data)
        queried_supplier = queried_suppliers[0]
        self.assertEqual(queried_supplier['supplierName'], 'Wholefoods')
        self.assertEqual(queried_supplier['address'], 'unknown')

        resp = self.app.get('/suppliers?rating=7')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_action_make_recommendation(self):
        """ Recommend a list of suppliers given a specific product id"""
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_supplier = json.loads(resp.data)
        new_supplier_id = new_supplier["_id"]["$oid"]
        new_supplier.pop('_id', None)
        new_supplier['productIdList'] = ['2','3','4','5','7']
        new_supplier['averageRating'] = 5
        new_supplier['supplierName'] = 'Wholefoods'
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.app.get('/suppliers/7/recommend')
        recommend_suppliers = json.loads(resp.data)
        supplier = recommend_suppliers[0]
        self.assertEqual(supplier['supplierName'],'Wholefoods')
        self.assertEqual(supplier['averageRating'],5)
        self.assertEqual(supplier['productIdList'],['2','3','4','5','7'])

    def test_not_found(self):
        """ Test Not Found Error Handle """
        test_supplier = SupplierFactory()
        resp = self.app.get('/suppliers/1234/recommend')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        """ Test Method Not Support Error Handle """
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers/1234/recommend')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_internal_error(self):
        """ Test Internal Error Handle """
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
