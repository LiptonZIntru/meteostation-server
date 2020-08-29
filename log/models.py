from django.db import models
from station.models import Station
# Create your models here.


class Log(models.Model):
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    temperature = models.FloatField()
    humidity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.station) + ": " + str(self.created_at)
