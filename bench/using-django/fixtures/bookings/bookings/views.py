from rest_framework import generics, permissions

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class RoomList(generics.ListAPIView):
    queryset = Room.objects.order_by("name")
    serializer_class = RoomSerializer


class BookingCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
