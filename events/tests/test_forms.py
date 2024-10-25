from django.test import TestCase
from ..forms import (
    EventBasicInfoForm,
    EventLocationForm,
    EventDetailsForm,
    EventRequirementsForm
)
from ..models import Event

class EventBasicInfoFormTest(TestCase):
    def test_valid_data(self):
        form = EventBasicInfoForm(data={
            'title': 'Sample Event',
            'description': 'Sample description',
            'event_type': 'meeting',  # Update to match the model's choice format
            'mode': 'online'
        })
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        form = EventBasicInfoForm(data={
            'description': 'Sample description',
            'event_type': 'Workshop',
            'mode': 'online'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Title can't be empty.", form.errors['title'])

    def test_missing_description(self):
        form = EventBasicInfoForm(data={
            'title': 'Sample Event',
            'event_type': 'meeting',
            'mode': 'online'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Description can't be empty.", form.errors['description'])

class EventLocationFormTest(TestCase):
    def test_valid_online_data(self):
        form = EventLocationForm(data={
            'location_country': 'Country',
            'location_city': 'City',
            'location_meeting_link': 'https://meeting.link'
        }, event_type='Workshop', mode='online')
        self.assertTrue(form.is_valid())

    def test_physical_address_hidden_in_online_mode(self):
        form = EventLocationForm(data={
            'location_country': 'Country',
            'location_city': 'City',
            'location_meeting_link': 'https://meeting.link',
        }, event_type='Workshop', mode='online')
        self.assertTrue(form.is_valid())
        self.assertNotIn('physical_address', form.errors)  # Should be ignored for online events

    def test_physical_address_required_for_in_person_mode(self):
        form = EventLocationForm(data={
            'location_country': 'Country',
            'location_city': 'City',
            'location_meeting_link': 'https://meeting.link'
        }, event_type='Workshop', mode='in_person')
        self.assertFalse(form.is_valid())
        self.assertIn("Physical address can't be empty.", form.errors['physical_address'])

class EventDetailsFormTest(TestCase):
    def test_valid_data(self):
        form = EventDetailsForm(data={
            'duration': '2',
            'max_participants': 100,
            'date': '2024-10-30T10:00',
            'registration_deadline': '2024-10-29T10:00',
            'ticket_price': 50.00
        })
        self.assertTrue(form.is_valid())

    def test_missing_duration(self):
        form = EventDetailsForm(data={
            'max_participants': 100,
            'date': '2024-10-30T10:00',
            'registration_deadline': '2024-10-29T10:00',
            'ticket_price': 50.00
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Duration can't be empty.", form.errors['duration'])

    def test_missing_ticket_price(self):
        form = EventDetailsForm(data={
            'duration': '2',
            'max_participants': 100,
            'date': '2024-10-30T10:00',
            'registration_deadline': '2024-10-29T10:00'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Ticket price can't be empty.", form.errors['ticket_price'])

class EventRequirementsFormTest(TestCase):
    def test_valid_data(self):
        form = EventRequirementsForm(data={
            'special_requirements': 'Projector, Wifi',
            'equipment_needed': 'Laptops, Whiteboard',
            'accommodation_provided': True,
            'refreshments_provided': True
        })
        self.assertTrue(form.is_valid())

    def test_missing_special_requirements(self):
        form = EventRequirementsForm(data={
            'equipment_needed': 'Laptops',
            'accommodation_provided': True,
            'refreshments_provided': True
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Special requirements can't be empty.", form.errors['special_requirements'])

    def test_missing_equipment_needed(self):
        form = EventRequirementsForm(data={
            'special_requirements': 'Projector',
            'accommodation_provided': True,
            'refreshments_provided': True
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Equipment needed can't be empty.", form.errors['equipment_needed'])
