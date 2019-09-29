import ffmpeg
import uuid
from django.core.management.base import BaseCommand
from django.conf import settings 

from api.videos.models import Video
from api.highlights.models import Highlight
from api.ffmpeg import concat_videos

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('match_id', type=int)

    def concat_videos(self, videos):
        input_video_paths = []
        for video in videos:
            input_video_paths.append(video.video.path)

        highlight_name = uuid.uuid4().hex

        return concat_videos(input_video_paths, highlight_name)

    def handle(self, *args, **options):
        match_id = options.get('match_id', None)
        print(f'creating highlight for match {match_id}...')
        
        videos = Video.objects.filter(match_id=match_id)
        
        highlight_file = self.concat_videos(videos)
        highlight = Highlight(
            preview=videos[0].preview,
            video=highlight_file,
            match_id=match_id,
        )
        highlight.save()
        
        current_time = 0
        for video in videos:
            highlight.fragments.add(video, through_defaults=dict(start_time=current_time))
            current_time += video.duration
