import datetime
import uuid
from django.db import models
from uuid import UUID
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from datetime import datetime
import django


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


class User(AbstractUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4(), unique=True, null=False, primary_key=True)
    username = models.CharField(unique=True, max_length=30, null=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"User -> {self.email}"


class CustomAccountManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = kwargs
        if user['username'] is None:
            raise TypeError('username field is mandatory')
        if user['email'] is None:
            raise TypeError('email field is mandatory')
        user['email'] = self.normalize_email(user['email'])
        user_data = self.model(
            username=user['username'],
            email=user['email']
        )
        user_data.set_password(user['password'])
        user_data.save()
        return user_data
    def create_superuser(self, **kwargs):
        user = kwargs
        if user['username'] is None:
            raise TypeError('username field is mandatory')
        if user['email'] is None:
            raise TypeError('email field is mandatory')
        if user.get('is_superuser') is not True:
            raise TypeError('You must provide True to is_superuser')
        user['email'] = self.normalize_email(user['email'])
        user_data = self.model(
            username=user['username'],
            email=user['email']
        )
        user_data.set_password(user['password'])
        user_data.save()
        return user_data