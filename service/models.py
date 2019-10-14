import logging
from flask import Flask
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, connect


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
    supplierName = StringField(required=True)
    address = StringField(required=False)
    productIdList = ListField(IntField(), required=False)
    averageRating = IntField(required=False)

    def __repr__(self):
        return '<Supplier %r>' % (self.supplierName)

    # def save(self):
    #     """
    #     Saves a Supplier to the data store
    #     """
    #     Supplier.logger.info('Saving %s', self.supplierName)
    #     self.save()

    def serialize(self):
        """ Serializes a Supplier into a dictionary """
        return {"supplierName": self.supplierName,
                "address": self.address,
                "averageRating" : self.averageRating, 
                "productIdList": self.productIdList}

    def deserialize(self, data):
        """
        Deserializes a Supplier from a dictionary
        Args:
            data (dict): A dictionary containing the Supplier data
        """
        try:
            self.supplierName = data['supplierName']
            self.address = data['address']
            self.averageRating = data['averageRating']
            # product = Product()
            self.productIdList = data['productIdList']
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
        db = connect('myDatabase')
        app.app_context().push()
        # db.create_all()

    @classmethod
    def all(cls):
        #This is a function to return all suppliers
        cls.logger.info('Processing all suppliers')
        return cls.objects()

    @classmethod
    def delete(cla, supplier_id):
        """ Delete a supplier by it's ID """
        cls.logger.info('Processing deleting for id %s', supplier_id)
        try:
            return cls.objects(id=supplier_id).delete()
        except DoesNotExist:
            return None

    @classmethod
    def find_by_name(cla, supplier_name):
        """ Find a supplier by it's name """
        cls.logger.info('Processing looking for name %s', supplier_name)
        try:
            return cls.objects.get(supplierName=supplier_name)
        except DoesNotExist:
            return None


    @classmethod
    def find(cls, supplier_id):
        """Retrieves a single supplier with a given id (supplierID) """

        cls.logger.info('Getting supplier with id: %s'.format(supplier_id))

        try:
            return cls.objects(id=supplier_id)
        except DoesNotExist:
            return None


"""
Test case for evaluating if the database is properly connected
Should be removed as the further development goes
"""
# sup1 = Supplier(supplierID=123, supplierName = 'Walmart', address='NYC', averageRating=5)
# sup1.save()

# res = Supplier.objects(supplierName='sup1').first()
# print(res.address)
