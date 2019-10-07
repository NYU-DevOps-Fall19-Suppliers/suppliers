"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
# from service.models import Pet

class SupplierFactory(factory.Factory):
    """ Creates fake suppliers for tests. """
    # class Meta:
    #      model = supplier
    id = factory.Sequence(lambda n: n)
    # name = factory.Faker('first_name')
    # category = FuzzyChoice(choices=['dog', 'cat', 'bird', 'fish'])
    # available = FuzzyChoice(choices=[True, False])

if __name__ == '__main__':
    for _ in range(10):
        supplier = SupplierFactory()
        print(supplier.serialize())
