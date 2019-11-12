"""
Supplier Steps

Steps file for suppliers.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

from os import getenv
import logging
import json
import requests
from behave import *

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))
