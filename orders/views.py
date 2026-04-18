from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})


def cart_view(request):
    cart = request.session.get("cart", [])

    cart_items = []
    total = Decimal("0.00")

    for index, item in enumerate(cart):
        quantity = int(item["quantity"])
        unit_price = Decimal(item["unit_price"])
        line_total = unit_price * quantity
        total += line_total

        cart_items.append({
            "index": index,
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


def remove_from_cart(request, item_index):
    cart = request.session.get("cart", [])

    if request.method == "POST":
        if 0 <= item_index < len(cart):
            removed_item = cart.pop(item_index)
            request.session["cart"] = cart
            messages.success(request, f"{removed_item['pizza_name']} removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

    return redirect("orders:cart")