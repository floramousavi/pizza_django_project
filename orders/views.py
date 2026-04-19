from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, OrderStatusForm
from .models import Order, OrderItem


def staff_required(user):
    return user.is_staff


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

        cart_item = {
            "index": index,
            "type": item["type"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        }

        if item["type"] == "pizza":
            cart_item.update({
                "name": item["pizza_name"],
                "size": item["pizza_size_name"],
                "toppings": item.get("toppings", []),
            })
        elif item["type"] == "drink":
            cart_item.update({
                "name": item["drink_name"],
                "size": item["drink_size"],
                "toppings": [],
            })

        cart_items.append(cart_item)

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

            item_name = removed_item.get("pizza_name") or removed_item.get("drink_name") or "Item"
            messages.success(request, f"{item_name} removed from cart.")
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

        cart_item = {
            "type": item["type"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        }

        if item["type"] == "pizza":
            cart_item.update({
                "name": item["pizza_name"],
                "size": item["pizza_size_name"],
                "toppings": item.get("toppings", []),
            })
        elif item["type"] == "drink":
            cart_item.update({
                "name": item["drink_name"],
                "size": item["drink_size"],
                "toppings": [],
            })

        cart_items.append(cart_item)

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

                if item["type"] == "pizza":
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

                elif item["type"] == "drink":
                    OrderItem.objects.create(
                        order=order,
                        drink_id=item["drink_id"],
                        quantity=quantity,
                        item_name_snapshot=f"{item['drink_name']} ({item['drink_size']})",
                        item_price_snapshot=unit_price,
                    )

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


@login_required
@user_passes_test(staff_required)
def staff_order_list(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "orders/staff_order_list.html", {"orders": orders})


@login_required
@user_passes_test(staff_required)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data["status"]
            order.save()
            messages.success(request, f"Order #{order.id} status updated.")
            return redirect("orders:staff_order_list")
    else:
        form = OrderStatusForm(initial={"status": order.status})

    return render(
        request,
        "orders/update_order_status.html",
        {
            "order": order,
            "form": form,
        },
    )