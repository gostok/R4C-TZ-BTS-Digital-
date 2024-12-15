from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration of the order management application.

    This class defines the settings for the "orders" application,
    including its name.
    The "ready" method imports signals related to this application.

    Attributes:
        name(str): the name of the application.
    """

    name = "orders"

    def ready(self):
        """
        Method called when the application is ready.

        Imports signals defined in the "orders.signals" module
        to ensure that they are registered when the application starts.
        """
        import orders.signals  # import signals
