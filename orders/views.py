from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Order
from .forms import OrderForm


class OrderListView(ListView):
    """
    View for displaying a list of orders and handling the form creating them.

    Uses the "Order" model to get all orders and displays them on the page
    using the "orders/index.html" template.
    Also handles POST requests for creating new orders.

    Attributes:
        model: the model used to get the data.
        template_name: the template used to display the data.
        context_object_name: the name of the context object for the template.
    """

    model = Order
    template_name = "orders/index.html"
    context_object_name = "orders"

    def get_queryset(self):
        """
        Gets all orders using the related "customer" model.

        Returns:
            QuerySet: all orders with customer data preloaded.
        """
        return Order.objects.select_related("customer")

    def get_context_data(self, **kwargs):
        """
        Adds a from for creating a new order to the context.

        Returns:
            dict: context object with orders and form.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = OrderForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request to create a new order.

        If the form is valid, a new order is created
        and redirected to the order list page.

        Returns:
            HttpResponse: response with redirect after successful creation
                            or displaying the form with validation errors.
        """
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("orders:order_list")

        context = {"form": form, "orders": self.get_queryset()}
        return render(request, self.template_name, context)
