from django.db import models

# Create your models here.

class Tavling(models.Model):
    TAVLING_TYPES = ((u'AG', u'Agilityklass'),
                     (u'HO', u'Hoppklass'))
    namn = models.CharField(max_length=200)
    typ = models.CharField(max_length=2, choices=TAVLING_TYPES)

class Lag(models.Model):
    tavling = models.ManyToManyField(Tavling, related_name='lag')
    ekipage = models.ManyToManyField(Ekipage, related_name='lag')

class Ekipage(models.Model):
    hundid = models.CharField(max_length=25)
    hundnamn = models.CharField(max_length=50)
    hundras = models.CharField(max_length=50)
    forare = models.CharField(max_length=50)

