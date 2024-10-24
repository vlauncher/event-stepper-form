from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from .forms import EventBasicInfoForm, EventDetailsForm, EventLocationForm, EventRequirementsForm
from .models import Event

class EventCreationWizard(SessionWizardView):
    form_list = [EventBasicInfoForm, EventDetailsForm, EventLocationForm, EventRequirementsForm]
    template_name = 'event_creation_step.html'

    def get_form(self, step=None, data=None, files=None):
        if step == '2':  # Assuming the location form is the 3rd step (index 2)
            event_type = self.get_cleaned_data_for_step('0')['event_type']  # Get event type from the first step
            mode = self.get_cleaned_data_for_step('0')['mode']  # Get mode from the first step
            return EventLocationForm(data, files, event_type=event_type, mode=mode)
        return super().get_form(step, data, files)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        current_step = int(self.steps.current)
        context.update({
            'step_prev': current_step - 1,
            'step_next': current_step + 1,
        })
        return context

    def done(self, form_list, **kwargs):
        event_data = {}
        for form in form_list:
            event_data.update(form.cleaned_data)
        event = Event.objects.create(**event_data, organizer=self.request.user)
        return redirect('home', pk=event.pk)
