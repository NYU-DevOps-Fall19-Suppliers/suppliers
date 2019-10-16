"""
Test __init__.py
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

class TestInit(unittest.TestCase):

    @patch('service.service.init_db')
    def test_init_db_exception(self, init_db_mock):
        """ Test a Exception raised in __init__ """
        init_db_mock.raiseError.side_effect = Mock(side_effect=Exception('Test'))
        with self.assertRaises(SystemExit) as cm:
            app.debug = False
            # disconnect('default')
            disconnect('testdb1')
            db = connect('testdb1')
            db.drop_database('testdb1')
            self.app = app.test_client()
            disconnect('testdb1')
        self.assertEqual(cm.exception.code, 4) 
