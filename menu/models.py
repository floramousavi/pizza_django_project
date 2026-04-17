from django.db import models


class PizzaSize(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    topping_extra_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Topping(models.Model):
    name = models.CharField(max_length=100, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    available = models.BooleanField(default=True)
    allowed_toppings = models.ManyToManyField(Topping, blank=True, related_name="pizzas")

    def __str__(self):
        return self.name


class Drink(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.size})"
