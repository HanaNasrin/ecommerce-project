from types import SimpleNamespace

from django.test import SimpleTestCase

from shop.context_processors import cart_count


class CartCountContextProcessorTests(SimpleTestCase):
    def test_cart_count_returns_total_quantity(self):
        request = SimpleNamespace(session={'cart': {'1': 2, '2': 1}})

        self.assertEqual(cart_count(request), {'cart_count': 3})
