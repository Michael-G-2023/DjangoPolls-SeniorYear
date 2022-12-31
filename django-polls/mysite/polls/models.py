# Create your models here.
import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dayandtime = models.DateField()
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " " + str(self.dayandtime) + " " + str(self.choice)