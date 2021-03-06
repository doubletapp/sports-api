from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    logo = models.CharField(max_length=255, null=False, blank=False)
    global_id = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.name