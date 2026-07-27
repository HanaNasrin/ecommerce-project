# from types import SimpleNamespace

# from django.test import SimpleTestCase

# from shop.context_processors import cart_count


# class CartCountContextProcessorTests(SimpleTestCase):
#     def test_cart_count_returns_total_quantity(self):
#         request = SimpleNamespace(session={'cart': {'1': 2, '2': 1}})

#         self.assertEqual(cart_count(request), {'cart_count': 3})




from django.test import TestCase
from .models import Category, Product

class ProductModelTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Electronics")

        Product.objects.create(
            category=category,
            name="Laptop",
            description="Gaming Laptop",
            price=50000,
            stock=10
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Laptop")
        self.assertEqual(product.price, 50000)