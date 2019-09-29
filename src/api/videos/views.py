import datetime

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from api.events.models import Event
from .models import Video, VideoEvent


def serialize_videos(videos, user_id):
    return [dict(
        id=video.id,
        preview_url=f'{settings.MEDIA_HOST}{video.preview.url}',
        video_url=f'{settings.MEDIA_HOST}{video.video.url}',
        match_id=video.match_id,
        user_id=video.user_id,
        is_liked=user_id in video.liked_by,
        likes_count=len(video.liked_by),
    ) for video in videos]


class VideosView(View):
    def get(self, request):
        params={}
        match_id = request.GET.get('match', None)
        user_id = request.GET.get('user', None)
        if match_id is not None:
            params['match_id']=match_id
        if user_id is not None:
            params['user_id']=user_id

        videos = Video.objects.filter(**params)
        return JsonResponse({
            'videos': serialize_videos(videos, request.user_id)
        }, status=200)

    def post(self, request):
        preview = request.FILES.get('preview', None)
        video = request.FILES.get('video', None)
        match_id = request.POST.get('match', None)
        start_real_time = request.POST.get('start_real_time', None)
        duration = request.POST.get('duration', None)
        
        video = Video(
            preview=preview,
            video=video,
            match_id=match_id,
            user_id=request.user_id,
            start_real_time=start_real_time,
            duration=duration,
        )
        video.save()

        video = Video.objects.get(id=video.id)

        end_real_time=video.start_real_time + datetime.timedelta(seconds=video.duration)
        for event in Event.objects.filter(match_id=video.match_id, time__gt=video.start_real_time, time__lt=end_real_time):
            time_shift=event.time-video.start_real_time
            video_event = VideoEvent(
                event=event,
                video=video,
                time_shift=time_shift.total_seconds(),
            )
            video_event.save()


        return JsonResponse({
            'success': True
        }, status=200)


class LikeVideoView(View):
    def post(self, request, id):
        video = Video.objects.get(id=id)
        liked_by = set(video.liked_by)
        liked_by.add(request.user_id)
        video.liked_by = list(liked_by)
        video.save()

        return JsonResponse({
            'success': True
        }, status=200)
