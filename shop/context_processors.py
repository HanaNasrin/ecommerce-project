def cart_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values()) if cart else 0
    return {'cart_count': total_items}
