from django.conf import settings
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    nightly_rate_cents = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings")
    check_in = models.DateField()
    nights = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)
    amount_cents = models.PositiveIntegerField()
    refunded_cents = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Refund(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name="refunds")
    amount_cents = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
