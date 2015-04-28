# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Tavling(models.Model):
    TAVLING_TYPES = ((u'AG', u'Agilityklass'),
                     (u'HO', u'Hoppklass'))
    namn = models.CharField("Tävlingsnamn", max_length=200)
    typ = models.CharField("Klass", max_length=2, choices=TAVLING_TYPES)
    reftid = models.DecimalField("Referenstid", max_digits=5, decimal_places=2, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.namn, self.typ)

class Ekipage(models.Model):
    hundid = models.CharField("Hundens registreringsnummer", max_length=25)
    hundnamn = models.CharField("Hundens namn", max_length=50)
    hundras = models.CharField("Hundens ras", max_length=50)
    forare = models.CharField("Förarens namn", max_length=50)

    def __unicode__(self):
        return "%s & %s <%s>" % (self.forare, self.hundnamn, self.hundid)

class Lag(models.Model):
    namn = models.CharField("Lagets namn", max_length=60)
    tavling = models.ManyToManyField(Tavling, related_name='lag')
    ekipage = models.ManyToManyField(Ekipage, related_name='lag')

    def __unicode__(self):
        return self.namn

class Resultat(models.Model):
    ekipage = models.ForeignKey(Ekipage)
    tavling = models.ForeignKey(Tavling)

    tid = models.DecimalField("Tid", max_digits=5, decimal_places=2)

    # FIXME: Find out whether "tidsfel" should be counted into this or automatically calculated.
    fel = models.DecimalField("Fel (exkl. tidsfel)", max_digits=5, decimal_places=2)

    def tidsfel(self):
        return max(0, self.tavling.reftid - self.tid)
