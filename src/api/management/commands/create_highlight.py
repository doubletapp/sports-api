from django.core.management.base import BaseCommand

from api.videos.models import Video
from api.highlights.models import Highlight

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('match_id', type=int)

    def handle(self, *args, **options):
        match_id = options.get('match_id', None)
        print(f'creating highlight for match {match_id}...')
        random_match_video = Video.objects.filter(match_id=match_id)[0]
        highlight = Highlight(
            preview=random_match_video.preview,
            video=random_match_video.preview,
            match_id=match_id,
        )
        highlight.save()
        highlight.fragments.set([random_match_video])
