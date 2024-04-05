from django.db import models

class Challenge(models.Model):
    #provider = models.IntegerField()
    start = models.DateField("start")
