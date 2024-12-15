from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    Administrative interface settings for the Order model.

    Attributes:
        list_display: Fields to display in the order list.
        search_fields: Fields to search by.
    """

    list_display = ("customer", "robot_serial")
    search_fields = ("customer__email", "robot_serial")

    def customer_email(seld, obj):
        """
        Returns the customer's email address to display in the admin panel.

        Parameters:
            obj: An instance of the Order model.

        Returns:
            str: Customer's email address.
        """
        return obj.customer.email

    customer_email.short_description = "Customer Email"


admin.site.register(Order, OrderAdmin)
