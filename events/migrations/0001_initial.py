# Generated by Django 5.1.2 on 2024-10-24 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("meeting", "Meeting"),
                            ("webinar", "Webinar"),
                            ("party", "Party"),
                        ],
                        default="meeting",
                        max_length=50,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("agenda", models.TextField(blank=True)),
                (
                    "location_country",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "location_city",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("location_meeting_link", models.URLField(blank=True, null=True)),
                (
                    "physical_address",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("in_person", "In-Person"),
                            ("online", "Online"),
                            ("hybrid", "Hybrid"),
                        ],
                        default="in_person",
                        max_length=20,
                    ),
                ),
                ("date", models.DateTimeField()),
                ("duration", models.DurationField()),
                ("accommodation_provided", models.BooleanField(default=False)),
                ("refreshments_provided", models.BooleanField(default=False)),
                ("max_participants", models.PositiveIntegerField()),
                ("contact_details", models.CharField(max_length=255)),
                (
                    "ticket_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("registration_deadline", models.DateTimeField()),
                ("special_requirements", models.TextField(blank=True, null=True)),
                ("equipment_needed", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="EventFacilitator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=255)),
                ("confirmed", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="EventInvitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invitee_email", models.EmailField(max_length=254)),
                (
                    "invitation_type",
                    models.CharField(
                        choices=[("guest", "Guest"), ("facilitator", "Facilitator")],
                        max_length=20,
                    ),
                ),
                ("is_accepted", models.BooleanField(default=False)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="EventParticipant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("registered_at", models.DateTimeField(auto_now_add=True)),
                ("has_attended", models.BooleanField(default=False)),
            ],
        ),
    ]
