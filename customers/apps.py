from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """
    Configuration of the customer management application.

    This class defines the settings for the "customers" application,
    including its name and other parameters.

    Attributes:
        name(str): the name of the application.
    """

    name = "customers"
