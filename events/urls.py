from django.urls import path
from .views import EventCreationWizard

urlpatterns = [
    path('create/', EventCreationWizard.as_view(), name='event_create'),
]
