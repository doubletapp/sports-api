from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    logo = models.CharField(max_length=255, null=False, blank=False)
    color = models.CharField(max_length=255, null=False, blank=False)
