from django.http import JsonResponse
from django.views import View

from .models import Highlight


def serialize_hightlights(highlights):
    return [dict(
        id=highlight.id,
    ) for highlight in highlights]


class HighlightsView(View):
    def get(self, request):
        highlights = Highlight.objects.all()
        return JsonResponse({
            'highlights': serialize_hightlights(highlights)
        }, status=200)
