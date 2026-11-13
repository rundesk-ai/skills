from django.urls import path

from .reports import OccupancyReport
from .views import BookingCreate, RoomList

urlpatterns = [
    path("rooms/", RoomList.as_view()),
    path("bookings/", BookingCreate.as_view()),
    path("reports/occupancy/", OccupancyReport.as_view()),
]
