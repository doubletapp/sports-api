import ffmpeg
import uuid
from django.core.management.base import BaseCommand
from django.conf import settings 

from api.videos.models import Video, VideoEvent
from api.highlights.models import Highlight, HighlightEvent
from api.ffmpeg import concat_videos, cut_video

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('match_id', type=int)

    def concat_videos(self, videos):
        input_video_paths = []
        for video in videos:
            path = cut_video(video['path'], video['start'], video['end'], uuid.uuid4().hex)
            input_video_paths.append(path)

        highlight_name = uuid.uuid4().hex

        return concat_videos(input_video_paths, highlight_name)

    def handle(self, *args, **options):
        match_id = options.get('match_id', None)
        # match_id = 9
        print(f'creating highlight for match {match_id}...')
        
        match_videos = Video.objects.filter(match_id=match_id)

        before_shift=8
        after_shift=12

        print(match_videos)
        fragments = []
        for match_video in match_videos:
            for video_event in VideoEvent.objects.filter(video_id=match_video.id):
                event_start_shift=max(0, video_event.time_shift-before_shift)
                event_end_shift=min(video_event.time_shift+after_shift, match_video.duration)
                fragments.append(dict(start=event_start_shift, end=event_end_shift, event=video_event.event, video=match_video))


        print(fragments)
        print('---')
        hightlight_events=dict()
        for fragment in fragments:
            if not fragment['event'].id in hightlight_events:
                hightlight_events[fragment['event'].id] = list()
            hightlight_events[fragment['event'].id].append(fragment)
        print(hightlight_events)


        videos = list()
        for he_by_event in hightlight_events.values():
            for he in he_by_event:
                videos.append(dict(
                    path=he['video'].video.path,
                    start=he['start'],
                    end=he['end'],
                ))





        highlight_file = self.concat_videos(videos)
        highlight = Highlight(
            preview=match_videos[0].preview,
            video=highlight_file,
            match_id=match_id,
        )
        highlight.save()
        #
        # current_time = 0
        # for video in videos:
        #     highlight.fragments.add(video, through_defaults=dict(start_time=current_time))
        #     current_time += video.duration
