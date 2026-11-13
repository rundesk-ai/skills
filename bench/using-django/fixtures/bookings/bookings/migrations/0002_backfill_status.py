from django.db import migrations


def confirm_blank_statuses(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    Booking.objects.filter(status="").update(status="confirmed")


class Migration(migrations.Migration):
    dependencies = [("bookings", "0001_initial")]

    operations = [migrations.RunPython(confirm_blank_statuses)]
