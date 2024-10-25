from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import Event, EventParticipant, EventInvitation, EventFacilitator

User = get_user_model()


class EventModelTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@example.com",
            first_name="Organizer",
            last_name="User",
            password="password123",
        )
        self.event = Event.objects.create(
            title="Test Event",
            organizer=self.organizer,
            description="An example event",
            date=timezone.now() + timezone.timedelta(days=1),
            duration=timezone.timedelta(hours=2),
            max_participants=50,
            contact_details="contact@example.com",
            registration_deadline=timezone.now() + timezone.timedelta(hours=23),
        )

    def test_event_string_representation(self):
        self.assertEqual(str(self.event), "Test Event")

    def test_is_past_property(self):
        self.assertFalse(self.event.is_past)
        self.event.date = timezone.now() - timezone.timedelta(days=1)
        self.event.save()
        self.assertTrue(self.event.is_past)

    def test_is_registration_open_property(self):
        self.assertTrue(self.event.is_registration_open)
        self.event.registration_deadline = timezone.now() - timezone.timedelta(hours=1)
        self.event.save()
        self.assertFalse(self.event.is_registration_open)


class EventParticipantModelTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@example.com",
            first_name="Organizer",
            last_name="User",
            password="password123",
        )
        self.participant = User.objects.create_user(
            email="participant@example.com",
            first_name="Participant",
            last_name="User",
            password="password123",
        )
        self.event = Event.objects.create(
            title="Test Event",
            organizer=self.organizer,
            description="An example event",
            date=timezone.now() + timezone.timedelta(days=1),
            duration=timezone.timedelta(hours=2),
            max_participants=50,
            contact_details="contact@example.com",
            registration_deadline=timezone.now() + timezone.timedelta(hours=23),
        )
        self.event_participant = EventParticipant.objects.create(
            event=self.event, user=self.participant
        )

    def test_event_participant_string_representation(self):
        self.assertEqual(
            str(self.event_participant), "participant@example.com - Test Event"
        )


class EventInvitationModelTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@example.com",
            first_name="Organizer",
            last_name="User",
            password="password123",
        )
        self.invitee_email = "invitee@example.com"
        self.event = Event.objects.create(
            title="Test Event",
            organizer=self.organizer,
            description="An example event",
            date=timezone.now() + timezone.timedelta(days=1),
            duration=timezone.timedelta(hours=2),
            max_participants=50,
            contact_details="contact@example.com",
            registration_deadline=timezone.now() + timezone.timedelta(hours=23),
        )
        self.invitation = EventInvitation.objects.create(
            event=self.event,
            inviter=self.organizer,
            invitee_email=self.invitee_email,
            invitation_type="guest",
        )

    def test_event_invitation_string_representation(self):
        self.assertEqual(
            str(self.invitation), "Invitation to invitee@example.com for Test Event"
        )

    def test_accept_invitation(self):
        self.invitation.accept()
        self.assertTrue(self.invitation.is_accepted)
        self.assertIsNotNone(self.invitation.accepted_at)


class EventFacilitatorModelTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email="organizer@example.com",
            first_name="Organizer",
            last_name="User",
            password="password123",
        )
        self.facilitator = User.objects.create_user(
            email="facilitator@example.com",
            first_name="Facilitator",
            last_name="User",
            password="password123",
        )
        self.event = Event.objects.create(
            title="Test Event",
            organizer=self.organizer,
            description="An example event",
            date=timezone.now() + timezone.timedelta(days=1),
            duration=timezone.timedelta(hours=2),
            max_participants=50,
            contact_details="contact@example.com",
            registration_deadline=timezone.now() + timezone.timedelta(hours=23),
        )
        self.event_facilitator = EventFacilitator.objects.create(
            event=self.event, facilitator=self.facilitator, role="Speaker"
        )

    def test_event_facilitator_string_representation(self):
        self.assertEqual(
            str(self.event_facilitator),
            "facilitator@example.com - Test Event (Speaker)",
        )

    def test_facilitator_confirmation(self):
        self.event_facilitator.confirmed = True
        self.event_facilitator.save()
        self.assertTrue(self.event_facilitator.confirmed)
