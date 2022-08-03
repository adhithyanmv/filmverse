from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length = 80, default=list)
    usermoviename = ArrayField(models.CharField(max_length = 100, default=list), blank=True)
    usermovieimage = ArrayField(models.CharField(max_length = 100, default=list), blank=True)
    usermovieid = ArrayField(models.IntegerField(default=list), blank=True)
    usermovietype = ArrayField(models.CharField(max_length = 100, default=list), blank=False)
    # pwd for superuser = bru7almbb
    # username = adhithyanmv
    # email = adhithyanmv7@gmail.com
    # virtual env = fil
    # a = Users.objects.create(username="adhithyan", usermoviename=["avengers", "thor"], usermovieimage=["ava.png", "eva.png"], usermovieid=[6868, 6969])