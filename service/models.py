import logging
from flask import Flask
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, connect
from mongoengine.errors import DoesNotExist, InvalidQueryError, ValidationError
from mongoengine.queryset.visitor import Q

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
    productIdList = ListField(StringField(), required=False)
    averageRating = IntField(required=False)

    def __repr__(self):
        return '<Supplier %r>' % (self.supplierName)

    # def save(self):
    #     """
    #     Saves a Supplier to the data store
    #     """
    #     Supplier.logger.info('Saving %s', self.supplierName)
    #     self.save()

    # Deprecated function. Use supplier.to_json() instead

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize mongoDB from the Flask app
        db = connect('myDatabase')
        app.app_context().push()

    @classmethod
    def all(cls):
        #This is a function to return all suppliers
        cls.logger.info('Processing all suppliers')
        return cls.objects()

    @classmethod
    def delete(cls, supplier_id):
        """ Delete a supplier by it's ID """
        cls.logger.info('Processing deleting for id %s', supplier_id)
        try:
            res = cls.objects(id=supplier_id).first()
        except ValidationError:
            return None
        res.delete()

    @classmethod
    def find_by_name(cls, supplier_name):
        """ Find a supplier by its name """
        cls.logger.info('Processing looking for name %s', supplier_name)
        try:
            res = cls.objects.get(supplierName=supplier_name)
        except ValidationError:
            return None
        return res


    @classmethod
    def find(cls, supplier_id):
        """Retrieves a single supplier with a given id (supplierID) """

        cls.logger.info('Getting supplier with id: {}'.format(supplier_id))

        try:
            res = cls.objects(id=supplier_id).first()
        except ValidationError:
            return None
        return res

    @classmethod
    def find_by_product(cls, product_id):
        """Retrieves a list of supplier with a given product id """
        cls.logger.info("Getting suppliers with product id: %s".format(product_id))
        try:
            res = cls.objects(productIdList__in=product_id)
        except ValidationError:
            return None
        return res

    @classmethod
    def find_by_rating(cls, rating):
        """Retrieves a list of supplier with a given rating score """
        cls.logger.info("Getting suppliers with ratting score greater than: %d".format(rating))
        try:
            res = cls.objects(averageRating__gte=3)
        except ValidationError:
            return None
        return res

    @classmethod
    def action_make_recommendation(cls, product_id):
        """Retrieves a list of supplier with a given rating score and product id """
        cls.logger.info("Getting suppliers with ratting score greater than: %s".format(product_id))
        try:
            res = cls.objects(Q(productIdList__in=product_id) & Q(averageRating__gte=3))
        except ValidationError:
            return None
        return res


    @classmethod
    def find_by_product(cls, product_id):
        """Retrieves a list of supplier with a given product id """
        cls.logger.info("Getting suppliers with product id: %s".format(product_id))
        return cls.objects(productIdList__in=product_id)

    @classmethod
    def find_by_rating(cls, rating):
        """Retrieves a list of supplier with a given rating score """
        cls.logger.info("Getting suppliers with ratting score greater than: %d".format(rating))
        return cls.objects(averageRating__gte=3)

    @classmethod
    def action_make_recommendation(cls, product_id):
        """Retrieves a list of supplier with a given rating score and product id """
        cls.logger.info("Getting suppliers with ratting score greater than: %s".format(product_id))
        return cls.objects(Q(productIdList__in=product_id) & Q(averageRating__gte=3))




"""
Test case for evaluating if the database is properly connected
Should be removed as the further development goes
"""
# sup1 = Supplier(supplierID=123, supplierName = 'Walmart', address='NYC', averageRating=5)
# sup1.save()

# res = Supplier.objects(supplierName='sup1').first()
# print(res.address)
