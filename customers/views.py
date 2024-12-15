from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Customer
from .forms import CustomerForm


class CustomerListView(ListView):
    """
    View for displaying a list of customers.

    Uses the "Customer" model to get all customers
    and displays them on the page using the template
    "customers/index.html".

    Attributes:
        model: the model used to get the data.
        template_name: the template used to display the data.
        context_object_name: the name of the context object for the template.
    """

    model = Customer
    template_name = "customers/index.html"
    context_object_name = "customers"


class CustomerCreateView(CreateView):
    """
    View for creating a new customer.

    Uses the "CustomerForm" from to process the data entered by the user.

    After successful creation of the customer,
    redirects to the customer list page.

    Attributes:
        model: model used to create the new object.
        form_class: form used to process the data.
        template_name: template used to display the form.
        success_url: url to redirect to after successful creation.
    """

    model = Customer
    form_class = CustomerForm
    template_name = "customers/index.html"
    success_url = reverse_lazy("customers:customer_list")

    def form_valid(self, form):
        """
        Handle a valid form.

        Called when the form has successfully validated.
        Can be overridden tp perform additional logic
        before saving the object.

        Returns:
            HttpResponse: the redirect response after successful creation.
        """
        return super().form_valid(form)
