from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class KMCar(models.Model):
    license_plate = models.ForeignKey(User, on_delete=models.CASCADE)
    user_use = models.CharField(max_length=255, null=False)
    km_today = models.FloatField(default=0)
    total_journey = models.FloatField(default=0)
    date = models.DateField(default=date.today())
    
    class Meta:
        verbose_name = 'KMCar'
        verbose_name_plural = 'KMCars'
    
    def __str__(self):
        return self.license_plate
    
class PriceOfChangeOil(models.Model):
    oil_chevron = models.FloatField(null=False)
    oil_havoline = models.FloatField(null=False)
    air_filter = models.FloatField(null=False)
    oil_filter = models.FloatField(null=False)
    fuel_filter = models.FloatField(null=False)
    water_trap = models.FloatField(null=False)

    class Meta:
        verbose_name = 'PriceOfChangeOil'
        verbose_name_plural = 'PricesOfChangeOils'
    
class TotalPaidOil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(null=False)
    date = models.DateField(default=True)
    
    class Meta:
        verbose_name = 'TotalPaidOil'
        verbose_name_plural = 'TotalPaidsOil'
    
    def __str__(self):
        return str(self.user)