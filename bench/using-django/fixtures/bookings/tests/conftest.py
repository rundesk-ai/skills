import datetime

import pytest
from rest_framework.test import APIClient

from accounts.models import User
from bookings.models import Booking, Room


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def member(db):
    return User.objects.create_user("member", email="member@shop.example", password="pw-member-1")


@pytest.fixture
def manager(db):
    return User.objects.create_user(
        "manager", email="manager@shop.example", password="pw-manager-1", role=User.Role.MANAGER
    )


@pytest.fixture
def room(db):
    return Room.objects.create(name="Harbour", nightly_rate_cents=12000)


@pytest.fixture
def make_booking(room):
    def make(user, nights=2, **extra):
        return Booking.objects.create(
            user=user,
            room=room,
            check_in=datetime.date(2026, 12, 1),
            nights=nights,
            amount_cents=room.nightly_rate_cents * nights,
            **extra,
        )

    return make
