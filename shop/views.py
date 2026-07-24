from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

# ---------------- Home Page ----------------

class HomeView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Product
    template_name = "shop/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()[:4]


# ---------------- Product List ----------------

class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.all()

        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


# ---------------- Product Detail ----------------

class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"


# ---------------- Cart Page ----------------

class CartView(TemplateView):
    template_name = "shop/cart.html"


# ---------------- Add to Cart ----------------

def add_to_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.add(product)

    return redirect("cart")

# ---------------- View Cart ----------------

def cart_view(request):

    cart = request.session.get("cart", {})

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        products.append({

            "product": product,

            "quantity": quantity,

            "subtotal": subtotal,

        })

    return render(

        request,

        "shop/cart.html",

        {

            "products": products,

            "total": total,

        },

    )


# ---------------- Update Cart ----------------

def update_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    quantity_value = request.POST.get("quantity") or request.GET.get("quantity") or 0

    try:
        quantity = int(quantity_value)
    except (ValueError, TypeError):
        quantity = 0

    cart.update(product, quantity)

    return redirect("cart")


# ---------------- Remove from Cart ----------------

def remove_from_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect("cart")



class CheckoutView(View):

    def get(self, request):

        form = CheckoutForm()

        return render(
            request,
            "shop/checkout.html",
            {
                "form": form
            }
        )

    def post(self, request):

        form = CheckoutForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "shop/checkout.html",
                {
                    "form": form
                }
            )

        cart = request.session.get("cart", {})
        if not cart:
            return redirect("cart")

        order = Order.objects.create(
            customer_name=form.cleaned_data["full_name"],
            customer_email=form.cleaned_data["email"],
            phone=form.cleaned_data["phone"],
            address=form.cleaned_data["address"],
            city=form.cleaned_data["city"],
            pincode=form.cleaned_data["pincode"],
        )

        items = []
        total = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

        request.session["cart"] = {}
        request.session.modified = True

        return render(
            request,
            "shop/order_success.html",
            {
                "order": order,
                "items": items,
                "total": total,
            }
        )
    


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "shop/register.html",
        {"form": form}
    )


@login_required
def profile(request):

    orders = Order.objects.filter(
        customer_email=request.user.email
    )

    return render(

        request,

        "shop/profile.html",

        {

            "orders": orders

        }

    )





@login_required
def payment(request):

    cart = request.session.get("cart", {})

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(
        request,
        "shop/payment.html",
        {
            "products": products,
            "total": total,
        }
    )