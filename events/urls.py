from django.urls import path
from .views import EventCreationWizard, EventListView, EventDetailView

urlpatterns = [
    path("create/", EventCreationWizard.as_view(), name="event_create"),
    path("", EventListView.as_view(), name="event_list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
]
