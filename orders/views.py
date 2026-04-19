from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CheckoutForm
from .models import Order, OrderItem


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


@login_required
def checkout_view(request):
    cart = request.session.get("cart", [])

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")

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

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                status=Order.STATUS_PENDING,
            )

            for item in cart:
                quantity = int(item["quantity"])
                unit_price = Decimal(item["unit_price"])

                order_item = OrderItem.objects.create(
                    order=order,
                    pizza_id=item["pizza_id"],
                    pizza_size_id=item["pizza_size_id"],
                    quantity=quantity,
                    item_name_snapshot=f"{item['pizza_name']} ({item['pizza_size_name']})",
                    item_price_snapshot=unit_price,
                )

                topping_names = item.get("toppings", [])
                if topping_names:
                    allowed_toppings = order_item.pizza.allowed_toppings.filter(name__in=topping_names)
                    order_item.selected_toppings.set(allowed_toppings)

            request.session["cart"] = []
            messages.success(request, f"Order #{order.id} placed successfully.")
            return redirect("orders:order_history")
    else:
        form = CheckoutForm()

    context = {
        "cart_items": cart_items,
        "total": total,
        "form": form,
    }
    return render(request, "orders/checkout.html", context)