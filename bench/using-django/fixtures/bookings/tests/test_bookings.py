def test_rooms_are_listed(api_client, room):
    response = api_client.get("/api/rooms/")
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "Harbour"


def test_member_can_book(api_client, member, room):
    api_client.force_authenticate(member)
    response = api_client.post(
        "/api/bookings/",
        {"room": room.pk, "check_in": "2026-12-01", "nights": 2, "amount_cents": 24000},
    )
    assert response.status_code == 201


def test_occupancy_report_for_managers(api_client, manager, member, make_booking):
    make_booking(member)
    api_client.force_authenticate(manager)
    response = api_client.get("/api/reports/occupancy/")
    assert response.status_code == 200
    assert response.json() == [{"room__name": "Harbour", "bookings": 1, "revenue_cents": 24000}]


def test_occupancy_report_hidden_from_members(api_client, member):
    api_client.force_authenticate(member)
    assert api_client.get("/api/reports/occupancy/").status_code == 403
