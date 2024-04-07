from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    title = models.TextField(blank=False, null=True)
    provider = models.TextField(blank=False, null=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    date_of_start = models.DateField(null=True, blank=True)
    challenge_url = models.TextField(blank=True)
    helper_address = models.TextField(blank=True)
    contact = models.TextField(blank=True)

class ProgressLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=False)
    completed = models.BooleanField(null=True, blank=True)
    billed = models.BooleanField (null=True, blank=True)

    def __str__(self):
        return self.user.username+str(self.date)

class Sololingo(models.Model):
    english_word = models.CharField(max_length=100)
    ukrainian_translation = models.CharField(max_length=100)

    def __str__(self):
        return self.english_word
