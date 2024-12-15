from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import Customer


class CustomerForm(forms.ModelForm):
    """
    Form for creating or editing a customer.

    This form is based on the "Customer" model
    and includes validation for the email field.
    The validation checks for uniqueness of the email
    and its correctness.

    Attributes:
        Meta: defines the model and fields that should be included in the form.
    """

    class Meta:
        model = Customer
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите email"}
            ),
        }

    def clean_email(self):
        """
        Validate the email field.

        Checks if the entered email already exists in the database.
        If the email already exists, a validation error is raised.
        Also checks if the email is in the correct format.

        Returns:
            str: a verified and valid email.

        Exceptions:
            ValidationError: if the email already exists or is invalid.
        """
        email = self.cleaned_data.get("email")

        # checking email uniqueness
        if Customer.objects.filter(email=email).exists():
            raise ValidationError(
                "Email уже существует. Пожалуйста, используйте другой email."
            )

        # additional email validity check
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError as ve:
            raise ve("Введите корректный email адрес.")

        return email
