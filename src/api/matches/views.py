from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import Match

from api.videos.models import Video, VideoEvent


def serialize_matches(matches):
    return [dict(
        id=match.id,
        start_datetime=match.start_datetime,
        home_team=dict(
            id=match.home_team.id,
            logo=match.home_team.logo,
            name=match.home_team.name,
            score=match.home_team_score
        ),
        away_team=dict(
            id=match.away_team.id,
            logo=match.away_team.logo,
            name=match.away_team.name,
            score=match.away_team_score
        ),
        status=match.status,
        minute=match.minute,
        events=[dict(
            id=event.id,
            type=event.type,
            real_time=event.time,
            match_time=event.match_time,
            team=event.team,
            player=dict(
                last_name=event.player_name,
                avatar=event.player_avatar,
            ),
            home_score=event.home_score,
            away_score=event.away_score,
            method_score=event.method_score,
            videos=[dict(
                id=video.id,
                preview_url=f'{settings.MEDIA_HOST}{video.preview.url}',
                video_url=f'{settings.MEDIA_HOST}{video.video.url}',
            ) for video in Video.objects.filter(
                id__in=VideoEvent.objects.filter(event=event).values_list('video', flat=True)
            )]
        ) for event in match.events.all()]
    ) for match in matches]


class MatchesView(View):
    def get(self, request):
        matches = Match.objects.all()
        return JsonResponse({
            'matches': serialize_matches(matches)
        }, status=200)