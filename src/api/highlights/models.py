from django.db import models


class Highlight(models.Model):
    preview = models.FileField(null=False, blank=False)
    video = models.FileField(null=False, blank=False)
    match = models.ForeignKey('api.Match', null=False, blank=False, on_delete=models.CASCADE)
    fragments = models.ManyToManyField('api.Video', through='api.HighlightFragment')

    def __str__(self):
        return f'{self.match.home_team.name} - {self.match.away_team.name}'


class HighlightFragment(models.Model):
    highlight = models.ForeignKey('api.Highlight', null=False, blank=False, on_delete=models.CASCADE)
    video = models.ForeignKey('api.Video', null=False, blank=False, on_delete=models.CASCADE)
    second = models.IntegerField(null=False)
