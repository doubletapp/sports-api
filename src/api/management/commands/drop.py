from django.core.management.base import BaseCommand
from api.matches.models import Match
from api.teams.models import Team
from api.events.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        Event.objects.all().delete()
        Team.objects.all().delete()
        Match.objects.all().delete()
