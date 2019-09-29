from django.contrib import admin

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'global_id', 'type', 'time', 'time_format', 'time_seconds', 'team', 'match_time')

admin.site.register(Event, EventAdmin)