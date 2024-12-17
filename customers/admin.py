from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    """
    Administrative interface settings for the Customer model.

    Attributes:
        list_display: Fields that will be displayed in the customer list.
        search_fields: Fields that can be searched.
    """

    list_display = ("id", "email")
    search_fields = ("email",)


admin.site.register(Customer, CustomerAdmin)
