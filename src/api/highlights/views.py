from django.http import JsonResponse
from django.views import View

from .models import Highlight, HighlightFragment


def serialize_hightlights(highlights):
    return [dict(
        id=highlight.id,
        preview_url=highlight.preview.url,
        video_url=highlight.video.url,
        match=dict(
            id=highlight.match.id,
            start_datetime=highlight.match.start_datetime,
            home_team=dict(
                id=highlight.match.home_team.id,
                logo=highlight.match.home_team.logo,
                name=highlight.match.home_team.name,
                # score=Int
            ),
            away_team=dict(
                id=highlight.match.away_team.id,
                logo=highlight.match.away_team.logo,
                name=highlight.match.away_team.name,
                # score=Int
            ),
        ),
        fragments=[dict(
            video_id=fragment.id,
            start_time=HighlightFragment.objects.get(highlight=highlight, video=fragment).second,
            user_id=fragment.user_id,
        ) for fragment in highlight.fragments.all()],
    ) for highlight in highlights]


class HighlightsView(View):
    def get(self, request):
        highlights = Highlight.objects.all().prefetch_related('fragments', 'match', 'match__home_team', 'match__away_team')
        return JsonResponse({
            'highlights': serialize_hightlights(highlights)
        }, status=200)
