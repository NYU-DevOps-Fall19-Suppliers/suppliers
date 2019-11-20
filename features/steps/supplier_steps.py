"""
Supplier Steps

Steps file for suppliers.feature

"""

from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

@given('the following suppliers')
def step_impl(context):
    """ Create supplier data for testing """
    headers = {'Content-Type': 'application/json'}
    create_url = context.base_url + '/suppliers'
    for row in context.table:
        products = row['productIdList'].split(",")
        productList = [product for product in products]
        data = {
            "supplierName": row['supplierName'],
            "address": row['address'],
            "productIdList": productList,
            "averageRating": row['averageRating']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data = payload, headers = headers)
        expect(context.resp.status_code).to_equal(201)

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@when('I create a supplier with name "{name}", address "{address}", and product "{productsItems}"')
def step_impl(context, name, address, productsItems):
    headers = {'Content-Type': 'application/json'}
    create_url = context.base_url + '/suppliers'
    products = productsItems.split(",")
    productList = [product for product in products]
    data = {
        "supplierName": name,
        "address": address,
        "productIdList": productList,
    }
    payload = json.dumps(data)
    context.resp = requests.post(create_url, data = payload, headers = headers)

@when('I list all suppliers')
def step_impl(context):
    """ Make a call to the base URL """
    create_url = context.base_url + '/suppliers'
    context.resp = requests.get(create_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.page_source).to_contain(message)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@then('I should get "{status_code}"')
def step_impl(context, status_code):
    status = int(status_code.split(" ")[0])
    expect(context.resp.status_code).to_equal(status)

