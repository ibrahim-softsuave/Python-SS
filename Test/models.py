from django.db import models
import datetime
from django.utils import timezone


class Questions(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateTimeField('date')

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question

class register(models.Model):
    email=models.EmailField(max_length=100,primary_key=True)
    user_name=models.CharField(max_length=50)
    phone_number=models.PositiveIntegerField()
    password=models.CharField(max_length=8,null=False,default=True)
