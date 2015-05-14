# -*- coding: utf-8 -*-
from django.db import models, connection
# Create your models here.
import logging
import operator

class Tavling(models.Model):
    TAVLING_TYPES = ((u'AG', u'Agilityklass'),
                     (u'HO', u'Hoppklass'))
    namn = models.CharField("Tävlingsnamn", max_length=200)

    # FIXME: nödvändigt?
    typ = models.CharField("Klass", max_length=2, choices=TAVLING_TYPES)

    # FIXME: nödvändigt?
    domare = models.CharField("Domare", max_length=100)

    # Definitivt nödvändigt
    reftid = models.DecimalField("Referenstid", max_digits=5, decimal_places=2, null=True, blank=True)

    # FIXME:
    #
    # plats
    # tid/datum

    def __unicode__(self):
        return "%s, %s" % (self.namn, self.typ)

    def deltagare(self):
        alla = {}
        for lag in self.lag.all():
            alla[lag] = {'deltagare': {}, 'resultat': None}
            alla[lag]['resultat'] = lag.resultat(self)
            for ekipage in lag.ekipage.all():
                try:
                    alla[lag]['deltagare'][ekipage] = Resultat.objects.get(ekipage=ekipage, tavling=self)
                except:
                    alla[lag]['deltagare'][ekipage] = None
        return alla

class Ekipage(models.Model):
    hundid = models.CharField("Hundens registreringsnummer", max_length=25)
    hundnamn = models.CharField("Hundens namn", max_length=50)
    hundras = models.CharField("Hundens ras", max_length=50)
    forare = models.CharField("Förarens namn", max_length=50)

    def __unicode__(self):
        return "%s & %s" % (self.forare, self.hundnamn)

class Lag(models.Model):
    namn = models.CharField("Lagets namn", max_length=60)
    tavling = models.ManyToManyField(Tavling, through='Laganmalan', related_name='lag')
    ekipage = models.ManyToManyField(Ekipage, related_name='lag')

    def __unicode__(self):
        return "%s" % self.namn

    def resultat(self, tavling):
        # Pick the three best results by the following criteria:
        #
        #  1. The lowest faults
        #  2. The fastest time
        #
        # There must be three results with a valid time (None time
        # means that the contestant was disqualified).
        #
        # Returns a {'tid': tid, 'fel': fel} dict with the combined
        # faults/time for the three best results.

        allresults = Resultat.objects\
                             .filter(tavling=tavling)\
                             .filter(ekipage__lag=self)
        print allresults
        n_all = len(allresults)

        # Incomplete result
        if n_all < 3:
                return {'tid': None, 'fel': None}

        # Limit to only valid results
        goodresults = allresults.exclude(tid=Resultat.RESULT_DISQUALIFIED)
        print goodresults
        n_good = len(goodresults)

        # FIXME: I suppose a team has no results until it's proven to
        # be disqualified, which happens when there's less than three
        # good results on four attempts.
        if n_good < 3:
            if n_all == 4:
                return {'tid': Resultat.RESULT_DISQUALIFIED,
                        'fel': Resultat.RESULT_DISQUALIFIED}
            else:
                return {'tid': None, 'fel': None}

        bestresults = goodresults.order_by('fel','tid')[:3]
        print bestresults
        return {'tid': sum([r.tid for r in bestresults]),
                'fel': sum([r.fel for r in bestresults])}

    def resultat_fel(self, tavling):
        return self.resultat(tavling)[0]

    def resultat_tid(self, tavling):
        return self.resultat(tavling)[1]


class Laganmalan(models.Model):
    tavling = models.ForeignKey(Tavling)
    lag = models.ForeignKey(Lag)
    startordning = models.IntegerField()

    def __unicode__(self):
        return "<Lag %s: Tavling %s>" % (self.lag, self.tavling)

class Resultat(models.Model):
    RESULT_DISQUALIFIED = -1

    ekipage = models.ForeignKey(Ekipage)
    tavling = models.ForeignKey(Tavling)

    tid = models.DecimalField("Tid", max_digits=5, decimal_places=2)
    teknikfel = models.DecimalField("Fel", max_digits=5, decimal_places=2,
                                    null=True, blank=True)

    def fel(self):
        """Returnerar tidsfel, DISQUALIFIED eller None för fel, disk eller
inget resultat registrerat."""
        if self.tid == self.RESULT_DISQUALIFIED:
            return self.RESULT_DISQUALIFIED

        elif self.tavling.reftid is None:
            return self.teknikfel

        else:
            return self.teknikfel + max(0, self.tid - self.tavling.reftid)


    def __unicode__(self):
        s = "%s och %s: " % (self.ekipage.forare, self.ekipage.hundnamn)
        if self.tid == self.RESULT_DISQUALIFIED:
            s += "disk"
        else:
            s += "%0.2fs, " % self.tid
            s += "%d fel" % self.fel()
        return s
