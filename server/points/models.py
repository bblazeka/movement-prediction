from django.db import models

class Point(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    objects = models.Manager()