"""
Test cases for Suppliers Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from werkzeug.exceptions import NotFound

# DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestSuppliers(unittest.TestCase):
    """ Test Cases for Pets """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        # app.debug = False
        # Set up the test database
        # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        a = 1

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Pet.init_db(app)
        # db.drop_all()    # clean up the last tests
        # db.create_all()  # make our sqlalchemy tables
        a = 1

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        pass

    def test_create_a_supplier(self):
        """ Create a supplier and assert that it exists """
        pass

    def test_add_a_supplier(self):
        """ Create a supplier and add it to the database """
        pass

 
    def test_find_supplier(self):
        """ Find a supplier by ID """
        pass

 
