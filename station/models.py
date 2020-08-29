from django.db import models

# Create your models here.


class Station(models.Model):
    ip = models.CharField(max_length=20)
    location = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.location:
            return str(self.ip) + ', ' + (self.location)
        return str(self.ip)
