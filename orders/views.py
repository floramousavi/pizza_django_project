from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})


def cart_view(request):
    cart = request.session.get("cart", [])

    cart_items = []
    total = Decimal("0.00")

    for item in cart:
        quantity = int(item["quantity"])
        unit_price = Decimal(item["unit_price"])
        line_total = unit_price * quantity
        total += line_total

        cart_items.append({
            "pizza_name": item["pizza_name"],
            "pizza_size_name": item["pizza_size_name"],
            "toppings": item["toppings"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        })

    context = {
        "cart_items": cart_items,
        "total": total,
    }
    return render(request, "orders/cart.html", context)