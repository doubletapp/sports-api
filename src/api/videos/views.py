from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import Video


def serialize_videos(videos):
    return [dict(
        id=video.id,
        preview_url=f'{settings.MEDIA_HOST}{video.preview.url}',
        video_url=f'{settings.MEDIA_HOST}{video.video.url}',
        match_id=video.match_id,
        user_id=video.user_id,
    ) for video in videos]


class VideosView(View):
    def get(self, request):
        videos = Video.objects.all()
        return JsonResponse({
            'videos': serialize_videos(videos)
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

        return JsonResponse({
            'success': True
        }, status=200)

