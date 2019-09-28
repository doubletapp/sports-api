from django.db import models
from api.events.enums import TeamType
from api.events.enums import MethodScoreType

class Event(models.Model):
    global_id = models.CharField(max_length=255, null=False, blank=False)
    time = models.DateTimeField(null=False, blank=False, db_index=True)
    type = models.CharField(max_length=255, null=False, db_index=True)
    team = models.CharField(max_length=20, choices=TeamType.choices(), null=True)
    match = models.ForeignKey('api.Match', null=False, blank=False, on_delete=models.CASCADE, related_name='events')

    match_time = models.IntegerField(null=True)

    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    player_name = models.CharField(max_length=255, null=True)
    player_avatar = models.CharField(max_length=255, null=True)
    # method_score = models.CharField(max_length=255, null=True, choices=MethodScoreType.choices())
    method_score = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.type}'
