from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class KMCar(models.Model):
    license_plate = models.ForeignKey(User, on_delete=models.CASCADE)
    user_use = models.CharField(max_length=255, null=False)
    km_today = models.FloatField(default=0)
    total_journey = models.FloatField(default=0)
    date = models.DateField(null=False)
    
    class Meta:
        verbose_name = 'KMCar'
        verbose_name_plural = 'KMCars'
    
    def __str__(self):
        return self.license_plate