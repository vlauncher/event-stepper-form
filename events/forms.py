from django import forms
from .models import Event

from django import forms

from django import forms
from .models import Event

class EventBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'mode']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
        }

from django import forms
from .models import Event

class EventBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'mode']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
        }

class EventLocationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['location_country', 'location_city', 'physical_address', 'location_meeting_link']
        widgets = {
            'location_country': forms.TextInput(attrs={'class': 'form-control'}),
            'location_city': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_address': forms.TextInput(attrs={'class': 'form-control'}),
            'location_meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        event_type = kwargs.pop('event_type', None)
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        # Adjust fields based on event type and mode
        if mode in ['online', 'hybrid']:
            self.fields['physical_address'].widget = forms.HiddenInput()  # Hide physical address
            self.fields['physical_address'].required = False  # Not required
        else:
            self.fields['location_meeting_link'].required = False  # Optional for in-person events

        # Optional: Set the physical address field to be required for in-person events
        if mode == 'in_person':
            self.fields['physical_address'].required = True  # Make physical address required
            self.fields['location_meeting_link'].required = False  # Optional for in-person events
            self.fields['location_meeting_link'].widget = forms.HiddenInput()  # Hide country





from django import forms
from .models import Event

class EventDetailsForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Event Date & Time"
    )
    registration_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Registration Deadline"
    )

    class Meta:
        model = Event
        fields = ['date', 'duration', 'max_participants', 'ticket_price', 'registration_deadline']




class EventRequirementsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['special_requirements', 'equipment_needed', 'accommodation_provided', 'refreshments_provided']
