from django.db import models

# don't forget...
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class userInformation(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class userChatInformation(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
