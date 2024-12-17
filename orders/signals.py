"""
signals.py

This module contains signals for handling events related to order and robot models.

Signals:
- notify_customers: Notifies customers via email when a new robot is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customers(sender, instance, created, **kwargs):
    """
    Notifies customers via email about the availability of a new robot.

    This signal is triggered after the Robot model instance is saved.

    If the instance is created (created=True), the function looks for all orders
    associated with the robot serial number and sends notifications to customers.

    Parameters:
        sender: The model class that sends the signal (Robot).
        instance: The model instance that was saved.
        created: A boolean flag indicating whether a new instance was created.
        kwargs: Additional arguments.
    """
    if created:
        # we receive all orders for this robot by serial number
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            send_notification_email(
                order.customer.email, instance.model, instance.version
            )


def send_notification_email(email, model, version):
    """
    Sends an email notification about the robot's availability.

    Parameters:
        email(str): The client's email address.
        model(str): The robot's model.
        version(str): The robot's version.
    """
    subject = f"{model}-{version} снова в наличие!"  # email header
    message = (
        f"Добрый день!\nНедавно вы интересовались нашим роботом модели {model}, версии {version}. "
        "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
    )  # email body
    send_mail(
        subject, message, "from@example.com", [email]
    )  # sending an email to a customer
