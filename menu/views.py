from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from orders.forms import AddPizzaToCartForm
from .models import Drink, Pizza


def home(request):
    return render(request, "menu/home.html")


def menu_list(request):
    pizzas = Pizza.objects.filter(available=True)
    drinks = Drink.objects.filter(available=True)

    context = {
        "pizzas": pizzas,
        "drinks": drinks,
    }
    return render(request, "menu/menu_list.html", context)


def pizza_detail(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id, available=True)

    if request.method == "POST":
        form = AddPizzaToCartForm(request.POST)
        form.fields["toppings"].queryset = pizza.allowed_toppings.filter(available=True)

        if form.is_valid():
            size = form.cleaned_data["pizza_size"]
            toppings = form.cleaned_data["toppings"]
            quantity = form.cleaned_data["quantity"]

            topping_count = toppings.count()
            unit_price = size.price + (size.topping_extra_price * topping_count)

            cart = request.session.get("cart", [])

            cart_item = {
                "type": "pizza",
                "pizza_id": pizza.id,
                "pizza_name": pizza.name,
                "pizza_size_id": size.id,
                "pizza_size_name": size.name,
                "quantity": quantity,
                "toppings": [t.name for t in toppings],
                "unit_price": str(unit_price),
            }

            cart.append(cart_item)
            request.session["cart"] = cart

            messages.success(request, f"{pizza.name} added to cart.")
            return redirect("orders:cart")
    else:
        form = AddPizzaToCartForm()
        form.fields["toppings"].queryset = pizza.allowed_toppings.filter(available=True)

    return render(
        request,
        "menu/pizza_detail.html",
        {
            "pizza": pizza,
            "form": form,
        },
    )


def add_drink_to_cart(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id, available=True)

    if request.method == "POST":
        cart = request.session.get("cart", [])

        cart_item = {
            "type": "drink",
            "drink_id": drink.id,
            "drink_name": drink.name,
            "drink_size": drink.size,
            "quantity": 1,
            "unit_price": str(drink.price),
        }

        cart.append(cart_item)
        request.session["cart"] = cart

        messages.success(request, f"{drink.name} ({drink.size}) added to cart.")

    return redirect("menu:menu_list")