from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Event(models.Model):

    MODE_CHOICES = [
        ("in_person", "In-Person"),
        ("online", "Online"),
        ("hybrid", "Hybrid"),
    ]

    EVENT_TYPE_CHOICES = [
        ("meeting", "Meeting"),
        ("webinar", "Webinar"),
        ("party", "Party"),
    ]
    event_type = models.CharField(
        max_length=50, choices=EVENT_TYPE_CHOICES, default="meeting"
    )
    organizer = models.ForeignKey(
        User, related_name="organized_events", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    agenda = models.TextField(blank=True)
    location_country = models.CharField(max_length=100, blank=True, null=True)
    location_city = models.CharField(max_length=100, blank=True, null=True)
    location_meeting_link = models.URLField(
        blank=True, null=True
    )  # for online/hybrid events
    physical_address = models.CharField(max_length=255, blank=True, null=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default="in_person")
    date = models.DateTimeField()
    duration = models.DurationField()
    accommodation_provided = models.BooleanField(default=False)
    refreshments_provided = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField()
    contact_details = models.CharField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    registration_deadline = models.DateTimeField()
    special_requirements = models.TextField(
        blank=True, null=True
    )  # Accessibility, technical setup
    equipment_needed = models.TextField(
        blank=True, null=True
    )  # e.g., projector, mic, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date < timezone.now()

    @property
    def is_registration_open(self):
        return self.registration_deadline > timezone.now()


class EventParticipant(models.Model):
    event = models.ForeignKey(
        Event, related_name="participants", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="registered_events", on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    has_attended = models.BooleanField(default=False)  # Track actual attendance

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"


class EventInvitation(models.Model):
    INVITATION_TYPE_CHOICES = [
        ("guest", "Guest"),
        (
            "facilitator",
            "Facilitator",
        ),  # Facilitators could be speakers, trainers, etc.
    ]

    event = models.ForeignKey(
        Event, related_name="invitations", on_delete=models.CASCADE
    )
    inviter = models.ForeignKey(
        User, related_name="sent_invitations", on_delete=models.CASCADE
    )
    invitee_email = models.EmailField()
    invitation_type = models.CharField(max_length=20, choices=INVITATION_TYPE_CHOICES)
    is_accepted = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)

    def accept(self):
        self.is_accepted = True
        self.accepted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Invitation to {self.invitee_email} for {self.event.title}"


class EventFacilitator(models.Model):
    event = models.ForeignKey(
        Event, related_name="facilitators", on_delete=models.CASCADE
    )
    facilitator = models.ForeignKey(
        User, related_name="facilitated_events", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=255)  # e.g., Speaker, Trainer, etc.
    confirmed = models.BooleanField(
        default=False
    )  # Facilitators can confirm their participation

    def __str__(self):
        return f"{self.facilitator.email} - {self.event.title} ({self.role})"
