from django.contrib import admin
from .models import Event, EventInvitation, EventParticipant, EventFacilitator


admin.site.register(Event)
admin.site.register(EventInvitation)
admin.site.register(EventParticipant)
admin.site.register(EventFacilitator)
