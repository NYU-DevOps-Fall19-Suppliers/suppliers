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
from mock import MagicMock, patch
from .suppliers_factory import SupplierFactory

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
# DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetServer(unittest.TestCase):
    """ Pet Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        # app.debug = False
        # initialize_logging(logging.INFO)
        # # Set up the test database
        # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """

    def tearDown(self):
        pass

    def _create_suppliers(self, count):
        """ Factory method to create pets in bulk """
        return 0

    def test_index(self):
        """ Test the Home Page """
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

    def test_create_supplier(self):
        """ Create a new supplier """
        pass

    def test_update_supplier(self):
        """ Update an existing Pet """
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
