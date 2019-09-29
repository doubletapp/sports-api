from django.db import models
from django.contrib.postgres.fields import ArrayField


class Video(models.Model):
    preview = models.FileField(null=False, blank=False)
    video = models.FileField(null=False, blank=False)
    match = models.ForeignKey('api.Match', null=False, blank=False, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255, blank=False, null=False)
    start_real_time = models.DateTimeField(null=False, blank=False)
    duration = models.FloatField(null=False, blank=False)
    events = models.ManyToManyField('api.Event', through='api.VideoEvent')
    liked_by = ArrayField(
        models.CharField(max_length=255, null=False, blank=False),
        default=list,
    )

    def __str__(self):
        return f'{self.user_id} - {self.start_real_time}'


class VideoEvent(models.Model):
    event = models.ForeignKey('api.Event', null=False, blank=False, on_delete=models.CASCADE)
    video = models.ForeignKey('api.Video', null=False, blank=False, on_delete=models.CASCADE)
    time_shift = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'{self.event.type}, {self.event.time}, {self.time_shift}'