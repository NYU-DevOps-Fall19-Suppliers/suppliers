from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'myDatabase',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)

class Product(db.Document):
    """
    Class that represents a product id
    """
    product_id = db.StringField(required=True)

class Supplier(db.Document):
    """
    Suppliers data schema: https://github.com/nyu-devops-fall19-suppliers/suppliers/issues/21
    """
    supplierName = db.StringField(required=True)
    address = db.StringField(required=True)
    productIdList = db.ListField(db.ReferenceField(Product))
    averageRating = db.IntField(required=True)

"""
Test case for evaluating if the database is properly connected
Should be removed as the further development goes
"""
sup1 = Supplier(supplierName='sup1', address='NYC', averageRating=5)
sup1.save()

res = Supplier.objects(supplierName='sup1').first()
print(res.address)
