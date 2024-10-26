from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from .forms import (
    EventBasicInfoForm,
    EventDetailsForm,
    EventLocationForm,
    EventRequirementsForm,
    EventConfirmationForm,
)
from .models import Event
from django.views.generic import ListView, DetailView
from .models import Event
from django.contrib import messages


class EventCreationWizard(SessionWizardView):
    form_list = [
        EventBasicInfoForm,
        EventDetailsForm,
        EventLocationForm,
        EventRequirementsForm,
        EventConfirmationForm,
    ]
    template_name = "event_creation_step.html"

    form_titles = {
        "0": "Basic Information",
        "1": "Event Details",
        "2": "Event Location",
        "3": "Event Requirements",
        "4": "Confirmation",
    }

    def get_template_names(self):
        """Set a special template for the confirmation step"""
        if self.steps.current == "4":
            return ["event_creation_confirmation.html"]
        return [self.template_name]

    def get_form(self, step=None, data=None, files=None):
        if step == "2":
            event_type = self.get_cleaned_data_for_step("0")["event_type"]
            mode = self.get_cleaned_data_for_step("0")["mode"]
            return EventLocationForm(data, files, event_type=event_type, mode=mode)
        return super().get_form(step, data, files)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        current_step = int(self.steps.current)
        if self.steps.current == "4":
            form_data = {
                self.form_titles[step]: self.get_cleaned_data_for_step(step)
                for step in self.get_form_list().keys()
                if self.get_cleaned_data_for_step(step)
            }
            context["form_data"] = form_data

        context.update(
            {
                "step_prev": current_step - 1,
                "step_next": current_step + 1,
            }
        )
        return context

    def render(self, form=None, **kwargs):
        """
        Override render to handle the special case of the summary step without a form
        """
        if self.steps.current == "4":  # Confirmation step
            context = self.get_context_data(form=form, **kwargs)
            return self.render_to_response(context)
        return super().render(form, **kwargs)

    def done(self, form_list, **kwargs):
        # Combine form data and create event
        event_data = {}
        for form in form_list[:-1]:  # Exclude the last form (confirmation)
            event_data.update(form.cleaned_data)

        event = Event.objects.create(**event_data, organizer=self.request.user)

        messages.success(self.request, "Your event has been successfully created!")
        return redirect("event_list")  # Redirect to your event list or detail page


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"
