import logging
from flask import Flask
# from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, connect
# from flask_mongoengine.wtf import model_form


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass
# class Product(db.Document):
#     """
#     Class that represents a product id
#     """
#     product_id = db.IntField(required=True)

class Supplier(Document):
    """
    Suppliers data schema: https://github.com/nyu-devops-fall19-suppliers/suppliers/issues/21
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    supplierID = IntField(required=True)
    supplierName = StringField(required=True)
    address = StringField(required=False)
    productIdList = ListField(IntField(), required=False)
    averageRating = IntField(required=False)

    def __repr__(self):
        return '<Supplier %r>' % (self.supplierName)

    def save(self):
        """
        Saves a Supplier to the data store
        """
        supplier.logger.info('Saving %s', self.supplierName)
        if not self.supplierID:
            self.save()

    def serialize(self):
        """ Serializes a Supplier into a dictionary """
        return {"supplierID": self.supplierID,
                "supplierNamee": self.supplierNamee,
                "address": self.address,
                "productIDList": self.productIDList}

    def deserialize(self, data):
        """
        Deserializes a Supplier from a dictionary

        Args:
            data (dict): A dictionary containing the Supplier data
        """
        try:
            self.supplierID = data['supplierID']
            self.supplierName = data['supplierName']
            self.address = data['address']
            self.averageRatingy = data['averageRating']
            # product = Product()
            # self.productIDList = data['productIDList']
        except KeyError as error:
            raise DataValidationError('Invalid supplier: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid supplier: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """       
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize mongoDB from the Flask app
        # db.init_app(app)
        db = connect('myDatabase')
        app.app_context().push()
        # db.create_all()



"""
Test case for evaluating if the database is properly connected
Should be removed as the further development goes
"""
# sup1 = Supplier(supplierID=123, supplierName = 'Walmart', address='NYC', averageRating=5)
# sup1.save()

# res = Supplier.objects(supplierName='sup1').first()
# print(res.address)
