from django import forms
from menu.models import PizzaSize, Topping


class AddPizzaToCartForm(forms.Form):
    pizza_size = forms.ModelChoiceField(
        queryset=PizzaSize.objects.all(),
        empty_label="Select a size",
        label="Pizza size"
    )
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.filter(available=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Extra toppings"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantity"
    )


class CheckoutForm(forms.Form):
    confirm_order = forms.BooleanField(
        required=True,
        label="I confirm that I want to place this order"
    )