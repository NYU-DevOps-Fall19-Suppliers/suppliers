"""
Pet API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import time
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
        # api_key = generate_apikey()
        # app.config['API_KEY'] = api_key

        # initialize_logging(logging.INFO)
        # Set up the test database
        # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        disconnect('default')
        global db
        global testdb_name    # For concurrency
        millis = int(round(time.time() * 1000))
        testdb_name = "testdb" + str(millis)
        DB_URI = "mongodb+srv://suppliers:s3cr3t@nyu-devops-yzcs4.mongodb.net/"+ testdb_name +"?retryWrites=true&w=majority"
        db = connect(testdb_name, host=DB_URI)
        db.drop_database(testdb_name)
        self.app = app.test_client()
        # self.headers = {
        #     'X-Api-Key': app.config['API_KEY']
        # }

    def tearDown(self):
        db.drop_database(testdb_name)
        disconnect(testdb_name)

    def _create_suppliers(self, count):
        """ Factory method to create suppliers in bulk """
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post('/suppliers',
                                 json=test_supplier.to_json(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test supplier')

            new_supplier = json.loads(resp.data.decode('utf-8'))
            test_supplier.id = new_supplier["_id"]["$oid"]
            # test_supplier.id = new_supplier["id"]
            suppliers.append(test_supplier)
        return suppliers

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        """ Test create a new supplier """

        resp = self.app.post('/suppliers')
        self.assertRaises(DataValidationError)

        test_supplier = Supplier()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json'
                             )
        self.assertRaises(DataValidationError)

        test_supplier = Supplier()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='wrong',
                             )
        self.assertRaises(DataValidationError)

        test_supplier = Supplier()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             )
        self.assertRaises(DataValidationError)

        test_supplier = SupplierFactory()
        self.assertNotEqual(test_supplier, None)
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json'
                             )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        #self.assertTrue(location != None)
        # Check the data is correct
        new_supplier = json.loads(resp.data.decode('utf-8'))
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
        """ Test update an existing supplier """
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json'
                             )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = json.loads(resp.data.decode('utf-8'))
        new_supplier_id = new_supplier["_id"]["$oid"]
        # new_supplier_id = new_supplier["id"]
        new_supplier.pop('_id', None)
        # new_supplier.pop('id', None)
        new_supplier['address'] = 'unknown'
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json'
                            )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_supplier = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(updated_supplier['address'], 'unknown')

        new_supplier_id = 0
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                        json=new_supplier,
                        content_type='application/json'
                        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_supplier_list(self):
        """ Test get a list of suppliers """
        self._create_suppliers(2)
        resp = self.app.get('/suppliers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(len(data), 2)

    def test_delete_supplier(self):
        """ Test delete a Supplier """
        test_supplier = self._create_suppliers(2)[0]

        resp = self.app.delete('/suppliers/{}'.format(test_supplier.id),
                               content_type='application/json'
                               )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data.decode('utf-8')), 0)
        # make sure they are deleted
        resp = self.app.get('/suppliers/{}'.format(test_supplier.id),
                            content_type='application/json'
                            )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_walmart_for_bdd_fix(self):
        """ Delete the walmart entry for the bdd test"""

        resp = self.app.delete('/suppliers/{}'.format("5dd5b9ced8704e4de9e"),
                               content_type='application/json'
                               )
        
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        

    def test_get_supplier(self):
        """ Test get a single supplier """

        supplier = self._create_suppliers(1)
        supplier = supplier[0]
        valid_id = supplier.id

        resp = self.app.get('/suppliers/' + valid_id)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        pass

    def test_get_supplier_not_found(self):
        """ Test get a supplier thats not found """
        resp = self.app.get('/suppliers/4f4381f4e779897a2c000009')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        pass

    def test_query_supplier_list_by_rating(self):
        """ Test query suppliers by rating """
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json'
                             )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = json.loads(resp.data.decode('utf-8'))
        new_supplier_id = new_supplier["_id"]["$oid"]
        new_supplier.pop('_id', None)
        # new_supplier_id = new_supplier["id"]
        # new_supplier.pop('id', None)
        new_supplier['supplierName'] = 'Wholefoods'
        new_supplier['address'] = 'unknown'
        new_supplier['averageRating'] = 6
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json'
                            )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        resp = self.app.get("/suppliers?rating=6")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        queried_suppliers = json.loads(resp.data.decode('utf-8'))
        queried_supplier = queried_suppliers[0]
        self.assertEqual(queried_supplier['supplierName'], 'Wholefoods')
        self.assertEqual(queried_supplier['address'], 'unknown')

        resp = self.app.get('/suppliers?rating=7')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.app.get("/suppliers?averageRating=6")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        queried_suppliers = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(len(queried_suppliers), 1)
        queried_supplier = queried_suppliers[0]
        self.assertEqual(queried_supplier['supplierName'], 'Wholefoods')

        resp = self.app.get('/suppliers?averageRating=7')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_action_make_recommendation(self):
        """ Test recommend a list of suppliers given a specific product id"""
        test_supplier = SupplierFactory()
        resp = self.app.post('/suppliers',
                             json=test_supplier.to_json(),
                             content_type='application/json'
                             )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_supplier = json.loads(resp.data.decode('utf-8'))
        new_supplier_id = new_supplier["_id"]["$oid"]
        new_supplier.pop('_id', None)
        # new_supplier_id = new_supplier["id"]
        # new_supplier.pop('id', None)
        new_supplier['productIdList'] = ['2','3','4','5','7']
        new_supplier['averageRating'] = 5
        new_supplier['supplierName'] = 'Wholefoods'
        resp = self.app.put('/suppliers/{}'.format(new_supplier_id),
                            json=new_supplier,
                            content_type='application/json'
                            )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.app.get('/suppliers/7/recommend')
        recommend_suppliers = json.loads(resp.data.decode('utf-8'))
        supplier = recommend_suppliers[0]
        self.assertEqual(supplier['supplierName'],'Wholefoods')
        self.assertEqual(supplier['averageRating'],5)
        self.assertEqual(supplier['productIdList'],['2','3','4','5','7'])

        resp = self.app.get('/suppliers/100/recommend')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_401_handler(self):
    #     """ Test 401 handler """
    #     test_supplier = SupplierFactory()
    #     resp = self.app.post('/suppliers')
    #     self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_404_handler(self):
        """ Test 404 handler """
        resp = self.app.get('/suppliers/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_405_handler(self):
        """ Test 405 handler """
        resp = self.app.delete('/suppliers')

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health(self):
        """ Test healthcheck """
        resp = self.app.get('/healthcheck')
        resp_json = json.loads(resp.data.decode('utf-8'))
        
        self.assertEqual(resp_json["message"], 'Healthy')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_api(self):
        """ Test apidoc """
        resp = self.app.get('/apidocs/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
