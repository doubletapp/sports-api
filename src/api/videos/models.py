from django.db import models


class Video(models.Model):
    preview_url = models.FileField(null=False, blank=False)
    video_url = models.FileField(null=False, blank=False)
    match = models.ForeignKey('api.Match', null=False, blank=False, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f'{self.home_team.name} - {self.away_team.name}'