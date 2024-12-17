from django.urls import path
from .views import CustomerListView, CustomerCreateView

app_name = "customers"

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer_list"),
    path(
        "add/", CustomerCreateView.as_view(), name="customer_add"
    ),  # path to add client
]
