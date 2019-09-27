from django.db import models


class Match(models.Model):
    start_datetime = models.DateTimeField(null=False, blank=False, db_index=True)
    city = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, null=False, blank=False)
    minute = models.CharField(max_length=255, null=False, blank=False)
    home_team = models.ForeignKey('api.Team', null=False, blank=False, on_delete=models.CASCADE, related_name='home_team_match')
    away_team = models.ForeignKey('api.Team', null=False, blank=False, on_delete=models.CASCADE, related_name='away_team_match')
    global_id = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.home_team.name} - {self.away_team.name}'
