"""
Test cases for Suppliers Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Supplier, DataValidationError
from service import app
# from flask_mongoengine import MongoEngine
from mongoengine import connect
from mongoengine.connection import disconnect

# DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestSuppliers(unittest.TestCase):
    """ Test Cases for Suppliers """
    db = None

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):      
        disconnect('default')
        global db
        db = connect('testdb')
        # self.app = app.test_client()
        db.drop_database('testdb')

    def tearDown(self):
        db.drop_database('testdb')
        disconnect('testdb')

    def test_create_a_supplier(self):
        """ Create a supplier and assert that it exists """
        supplier = Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3'])
        self.assertTrue(supplier != None)
        self.assertEqual(supplier.supplierName, "Walmart")
        self.assertEqual(supplier.address, "NYC")
        self.assertEqual(supplier.averageRating, 5)
        self.assertEqual(supplier.productIdList, ['1','2','3'])

    def test_add_a_supplier(self):
        """ Create a supplier and add it to the database """
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 0)
        supplier = Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3'])
        self.assertTrue(supplier != None)
        self.assertEqual(supplier.id, None)
        supplier.save()
        # Asert that it was assigned an id and shows up in the database
        # self.assertEqual(supplier.id, 1)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)
        self.assertNotEqual(supplier.id, None)

    def test_update_a_supplier(self):
        """ Update a supplier """
        supplier = Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3'])
        supplier.save()
        self.assertNotEqual(supplier.id, None)
        old_id = supplier.id
        # Change it an save it
        supplier.supplierName = "Costco"
        supplier.save()
        self.assertEqual(supplier.id, old_id)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].supplierName, "Costco")
        # pass

    def test_delete_a_supplier(self):
        """ Delete a Supplier """
        supplier = Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3'])
        supplier.save()
        self.assertEqual(len(Supplier.all()), 1)
        # delete the supplier and make sure it isn't in the database
        supplier.delete(supplier.id)
        self.assertEqual(len(Supplier.all()), 0)
    
    def test_list_all_supplier(self):
        """ Return a list of suppliers """
        Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3']).save()
        Supplier(supplierName="Costco", address="SF", averageRating=2, productIdList = ['1','3','4']).save()
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 2)
        self.assertEqual(suppliers[0].supplierName, 'Walmart')
        self.assertEqual(suppliers[1].supplierName, 'Costco')

    def test_query_by_name(self):
        """ Return a supplier given a name """
        Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3']).save()
        Supplier(supplierName="Costco", address="SF", averageRating=2, productIdList = ['1','3','4']).save()
        supplier = Supplier.find_by_name("Walmart")
        self.assertEqual(supplier.address, "NYC")
        self.assertEqual(supplier.averageRating, 5)
        self.assertEqual(supplier.productIdList, ['1','2','3'])
    
    def test_query_by_product(self):
        Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3']).save()
        Supplier(supplierName="Costco", address="SF", averageRating=2, productIdList = ['1','3','4']).save()
        suppliers = Supplier.find_by_product("4")
        supplier = suppliers[0]
        self.assertEqual(supplier.supplierName, "Costco")
        self.assertEqual(supplier.address, "SF")
        self.assertEqual(supplier.averageRating, 2)
        self.assertEqual(supplier.productIdList, ['1','3','4'])

    def test_query_by_rating(self):
        Supplier(supplierName="Walmart", address="NYC", averageRating=5, productIdList = ['1','2','3']).save()
        Supplier(supplierName="Costco", address="SF", averageRating=2, productIdList = ['1','3','4']).save()
        suppliers = Supplier.find_by_rating(5)
        supplier = suppliers[0]
        self.assertEqual(supplier.supplierName, "Walmart")
        self.assertEqual(supplier.address, "NYC")
        self.assertEqual(supplier.averageRating, 5)
        self.assertEqual(supplier.productIdList, ['1','2','3'])


