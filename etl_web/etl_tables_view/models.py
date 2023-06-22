from django.db import models

# Create your models here.

class DimParty(models.Model):
    partyKey = models.IntegerField(primary_key=True)
    partyId = models.IntegerField(max_length=32)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    dateOfBirth = models.DateTimeField
    gender = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postalCode = models.IntegerField
    CityName = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    email = models.EmailField

    def __str__(self):
        return self.FirstName

