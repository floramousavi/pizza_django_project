from django.shortcuts import render
from .models import Pizza, Drink


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

