from django.http import JsonResponse
from django.views import View

from .models import Match


def serialize_matches(matches):
    return [dict(
        id=match.id,
        start_datetime=match.start_datetime,
        home_team=dict(
            id=match.home_team.id,
            logo=match.home_team.logo,
            name=match.home_team.name,
            # score=Int
        ),
        away_team=dict(
            id=match.home_team.id,
            logo=match.home_team.logo,
            name=match.home_team.name,
            # score=Int
        ),
        status=match.status,
        minute=match.minute,
        # events=[
        #     {
        #         id=Int,
        #         type=EventType,
        #         real_time=Date,
        #         match_time=Date
        #     }
        # ]
    ) for match in matches]


class MatchesView(View):
    def get(self, request):
        matches = Match.objects.all()
        return JsonResponse({
            'matches': serialize_matches(matches)
        }, status=200)