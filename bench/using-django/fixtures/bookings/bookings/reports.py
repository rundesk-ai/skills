from django.db.models import Count, Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking


class OccupancyReport(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        rows = (
            Booking.objects.filter(status=Booking.Status.CONFIRMED)
            .values("room__name")
            .annotate(bookings=Count("id"), revenue_cents=Sum("amount_cents"))
            .order_by("room__name")
        )
        return Response(list(rows))
