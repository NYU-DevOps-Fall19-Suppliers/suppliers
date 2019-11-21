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

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.page_source).to_contain(message)

@then('I should see the message "{message}"')
def step_impl(context, message):
    expect(context.driver.page_source).to_contain(message)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@then('I should get "{status_code}"')
def step_impl(context, status_code):
    status = int(status_code.split(" ")[0])
    expect(context.resp.status_code).to_equal(status)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@when('I change "{field}" to "{value}"')
def step_impl(context, field, value):
    # element = context.driver.find_element_by_id(field)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, field))
    )
    element.clear()
    element.send_keys(value)

@when('I copy from the "{field}" field')
def step_impl(context, field):
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, field))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Copy: {}'.format(context.clipboard))


@when('I paste to the "{field}" field')
def step_impl(context, field):
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, field))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then('I should see "{value}" in the "{field}" field')
def step_impl(context, field, value):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, field), value
        )
    )
    expect(found).to_be(True)

@then('I should see "{name}" in the results')
def step_impl(context, name):
    # element = context.driver.find_element_by_id('search_results')
    # expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)
