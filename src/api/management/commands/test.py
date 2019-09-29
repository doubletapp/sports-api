import datetime
from django.core.management.base import BaseCommand
from api.matches.models import Match
from api.teams.models import Team
from api.events.models import Event
from api.videos.models import Video, VideoEvent


class Command(BaseCommand):
    def handle(self, *args, **options):
        # print(VideoEvent.objects.all())
        # return

        video_id=8
        video = Video.objects.get(id=video_id)
        VideoEvent.objects.filter(video_id=video.id).delete()

        end_real_time=video.start_real_time + datetime.timedelta(seconds=video.duration)
        for event in Event.objects.filter(match_id=video.match_id, time__gt=video.start_real_time, time__lt=end_real_time):
            time_shift=event.time-video.start_real_time
            video_event = VideoEvent(
                event=event,
                video=video,
                time_shift=time_shift.total_seconds(),
            )
            video_event.save()
            print(video_event)
