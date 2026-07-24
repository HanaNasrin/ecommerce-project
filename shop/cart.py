class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product):

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1

        self.save()
    

    def save(self):

        self.session.modified = True

    def update(self, product, quantity):

        product_id = str(product.id)

        if quantity > 0:

            self.cart[product_id] = quantity

        else:

            del self.cart[product_id]

        self.save()

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.save()