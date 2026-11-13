from django.contrib import admin

from .models import Booking, Refund, Room

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Refund)
