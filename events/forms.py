from django import forms
from .models import Event
from datetime import timedelta


class EventBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "event_type", "mode"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "event_type": forms.Select(attrs={"class": "form-select"}),
            "mode": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "title": {"required": "Title can't be empty."},
            "description": {"required": "Description can't be empty."},
            "event_type": {"required": "Event type can't be empty."},
            "mode": {"required": "Mode can't be empty."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Event Title"
        self.fields["description"].label = "Event Description"
        self.fields["event_type"].label = "Event Type"
        self.fields["mode"].label = "Event Mode"


class EventLocationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "location_country",
            "location_city",
            "physical_address",
            "location_meeting_link",
        ]
        widgets = {
            "location_country": forms.TextInput(attrs={"class": "form-control"}),
            "location_city": forms.TextInput(attrs={"class": "form-control"}),
            "physical_address": forms.TextInput(attrs={"class": "form-control"}),
            "location_meeting_link": forms.URLInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "location_country": {"required": "Country can't be empty."},
            "location_city": {"required": "City can't be empty."},
            "physical_address": {"required": "Physical address can't be empty."},
            "location_meeting_link": {"required": "Meeting link can't be empty."},
        }

    def __init__(self, *args, **kwargs):
        event_type = kwargs.pop("event_type", None)
        mode = kwargs.pop("mode", None)
        super().__init__(*args, **kwargs)

        # Adjust fields based on event type and mode
        if mode in ["online", "hybrid"]:
            self.fields["physical_address"].widget = forms.HiddenInput()
            self.fields["physical_address"].required = False
        else:
            self.fields["location_meeting_link"].required = False

        if mode == "in_person":
            self.fields["physical_address"].required = True
            self.fields["location_meeting_link"].widget = forms.HiddenInput()


class EventDetailsForm(forms.ModelForm):
    duration = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Duration (eg. 1 hour)",
        error_messages={"required": "Duration can't be empty."},
    )
    max_participants = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Maximum Participants",
        error_messages={"required": "Max participants can't be empty."},
    )
    date = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        label="Event Date & Time",
        error_messages={"required": "Event date and time can't be empty."},
    )
    registration_deadline = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        label="Registration Deadline",
        error_messages={"required": "Registration deadline can't be empty."},
    )

    class Meta:
        model = Event
        fields = [
            "date",
            "duration",
            "max_participants",
            "ticket_price",
            "registration_deadline",
        ]
        error_messages = {
            "ticket_price": {"required": "Ticket price can't be empty."},
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        registration_deadline = cleaned_data.get("registration_deadline")

        if date and registration_deadline:
            if registration_deadline >= date:
                raise forms.ValidationError(
                    "Registration deadline must be before the event date."
                )
        return cleaned_data

    def clean_duration(self):
        duration_str = self.cleaned_data["duration"]

        # Parse '1 hour', '30 minutes', etc., to a timedelta object.
        try:
            time_units = duration_str.lower().split()
            if "day" in time_units[1]:
                duration = timedelta(days=int(time_units[0]))
            elif "hour" in time_units[1]:
                duration = timedelta(hours=int(time_units[0]))
            elif "minute" in time_units[1]:
                duration = timedelta(minutes=int(time_units[0]))
            else:
                raise ValueError("Invalid duration format.")

            return duration

        except (IndexError, ValueError):
            raise forms.ValidationError(
                "Invalid duration format. Use 'X day(s)', 'X hour(s)', or 'X minute(s)'."
            )


class EventRequirementsForm(forms.ModelForm):
    special_requirements = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        error_messages={"required": "Special requirements can't be empty."},
    )
    equipment_needed = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        error_messages={"required": "Equipment needed can't be empty."},
    )
    accommodation_provided = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    refreshments_provided = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Event
        fields = [
            "special_requirements",
            "equipment_needed",
            "accommodation_provided",
            "refreshments_provided",
        ]


class EventConfirmationForm(forms.Form):
    pass
