"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Supplier

class SupplierFactory(factory.Factory):
    """ Creates fake suppliers for tests. """
    class Meta:
         model = Supplier
    # supplierID = factory.Sequence(lambda n: n)
    supplierName = FuzzyChoice(choices=['Walmart', 'Costco', 'Ikea', 'Apple', 'Microsoft'])
    address = FuzzyChoice(choices=['NYC', 'LA', 'SF', 'Seattle'])
    averageRating = FuzzyChoice(choices=[1,2,3,4,5])
    productIdList = FuzzyChoice(choices=[[1,2,3],[2,3,4,5]])

if __name__ == '__main__':
    for _ in range(10):
        supplier = SupplierFactory()
        print(supplier.serialize())
