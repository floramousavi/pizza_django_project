from django.contrib import admin
from .models import PizzaSize, Topping, Pizza, Drink


@admin.register(PizzaSize)
class PizzaSizeAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "topping_extra_price")


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ("name", "available")
    list_filter = ("available",)
    search_fields = ("name",)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ("name", "available")
    list_filter = ("available",)
    search_fields = ("name",)
    filter_horizontal = ("allowed_toppings",)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "price", "available")
    list_filter = ("available", "size")
    search_fields = ("name",)
