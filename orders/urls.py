from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("history/", views.order_history, name="order_history"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:item_index>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("staff/", views.staff_order_list, name="staff_order_list"),
    path("staff/<int:order_id>/update/", views.update_order_status, name="update_order_status"),
]