from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form for creating or editing an order.

    This form is based on the "Order" model
    and includes fields for selecting a customer
    and entering the robot serial number.

    Attributes:
        Meta: defines the model and fields that should be included in the form.
    """

    class Meta:
        model = Order
        fields = ["customer", "robot_serial"]
        widgets = {
            "robot_serial": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите серийный номер робота",
                }
            ),
        }
