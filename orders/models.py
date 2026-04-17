from django.conf import settings
from django.db import models
from menu.models import Pizza, Drink, PizzaSize, Topping


class Order(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_PREPARING = "Preparing"
    STATUS_COMPLETED = "Completed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)
    pizza_size = models.ForeignKey(PizzaSize, on_delete=models.SET_NULL, null=True, blank=True)
    selected_toppings = models.ManyToManyField(Topping, blank=True)

    quantity = models.PositiveIntegerField(default=1)

    item_name_snapshot = models.CharField(max_length=150)
    item_price_snapshot = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Item #{self.id} in Order #{self.order.id}"