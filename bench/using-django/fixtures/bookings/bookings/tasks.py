from celery import shared_task
from django.core.mail import send_mail

from .models import Booking


@shared_task
def send_refund_email(booking_id):
    booking = Booking.objects.select_related("user").get(pk=booking_id)
    send_mail(
        "Your refund is on its way",
        f"We refunded {booking.refunded_cents / 100:.2f} for booking {booking.pk}.",
        None,
        [booking.user.email],
    )
