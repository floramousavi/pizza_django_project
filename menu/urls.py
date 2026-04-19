from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/pizza/<int:pizza_id>/", views.pizza_detail, name="pizza_detail"),
    path("menu/drink/<int:drink_id>/add/", views.add_drink_to_cart, name="add_drink_to_cart"),
]