from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class usersCars(models.Model):
    user = models.CharField(max_length=255, null=False)
class moreInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(max_length=255, null=False)
    vin = models.CharField(max_length=255, null=False)
    property = models.CharField(max_length=255, null=False)
    usersCar = models.ManyToManyField(usersCars, null=False)

