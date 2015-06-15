# -*- coding: utf-8 -*-
from django.db import models, connection
# Create your models here.
import logging
import operator

# ----------------------------------------

class Klass(models.Model):
    namn = models.CharField("Klassnamn", max_length=200)
    domare = models.CharField("Domare", max_length=100)
    reftid = models.DecimalField("Referenstid", max_digits=5, decimal_places=2, null=True, blank=True)
    plats = models.CharField("Plats", max_length=50)
    tid = models.DateField("Datum")

    def __unicode__(self):
        return "%s, %s, %s" % (self.namn, self.plats, self.tid)

    def deltagare(self):
        alla = []
        for lag in self.lag.all():

            _a = {'lag': lag,
                  'deltagare': [],
                  'resultat': lag.resultat(self)}
            for ekipage in lag.ekipage.all():
                _r = None
                try:
                    _r = Resultat.objects.get(tavling=self, ekipage=ekipage)
                except:
                    pass

                _a['deltagare'].append({'ekipage': ekipage,
                                        'resultat': _r})

            _a['deltagare'].sort(key=operator.itemgetter('resultat'))
            alla.append(_a)

        a = [SortableResult(x['resultat']['fel'], x['resultat']['tid']) for x in alla]
        print a
        print sorted(a)
        return sorted(alla, key=lambda x: SortableResult(x['resultat']['fel'], x['resultat']['tid']))

# ----------------------------------------

class Ekipage(models.Model):
    hundid = models.CharField("Hundens registreringsnummer", max_length=25)
    hundnamn = models.CharField("Hundens namn", max_length=50)
    hundras = models.CharField("Hundens ras", max_length=50)
    forare = models.CharField("Förarens namn", max_length=50)

    def __unicode__(self):
        return "%s & %s" % (self.forare, self.hundnamn)

# ----------------------------------------

class Lag(models.Model):
    namn = models.CharField("Lagets namn", max_length=60)
    tavling = models.ManyToManyField(Klass, through='Laganmalan', related_name='lag')
    ekipage = models.ManyToManyField(Ekipage, through='LagEkipage', related_name='lag')

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
        n_all = allresults.count()

        # Incomplete result
        if n_all < 3:
                return {'tid': None, 'fel': None}

        # Limit to only valid results
        goodresults = allresults.exclude(tid=Resultat.RESULT_DISQUALIFIED)
        n_good = goodresults.count()

        # FIXME: I suppose a team has no results until it's proven to
        # be disqualified, which happens when there's less than three
        # good results on four attempts.
        if n_good < 3:
            if n_all == 4:
                return {'tid': Resultat.RESULT_DISQUALIFIED,
                        'fel': Resultat.RESULT_DISQUALIFIED}
            else:
                return {'tid': None, 'fel': None}

        bestresults = sorted(goodresults, key=lambda x: (x.fel(), x.tid))[:3]
        return {'tid': sum([r.tid for r in bestresults]),
                'fel': sum([r.fel() for r in bestresults])}

    def resultat_fel(self, tavling):
        return self.resultat(tavling)[0]

    def resultat_tid(self, tavling):
        return self.resultat(tavling)[1]

# ----------------------------------------

class Laganmalan(models.Model):
    tavling = models.ForeignKey(Klass)
    lag = models.ForeignKey(Lag)
    startordning = models.IntegerField()

    def __unicode__(self):
        return "<Lag %s: Klass %s>" % (self.lag, self.tavling)

# ----------------------------------------

class LagEkipage(models.Model):
    ekipage = models.ForeignKey(Ekipage)
    lag = models.ForeignKey(Lag)
    startnummer = models.CharField(maxlength=1)

    def __unicode__(self):
        return "<Lag %s >" % (self.lag.startordning, self.tavling)

# ----------------------------------------

class Resultat(models.Model):
    RESULT_DISQUALIFIED = -1

    ekipage = models.ForeignKey(Ekipage)
    tavling = models.ForeignKey(Klass)

    diskvalificerad = models.BooleanField("Diskvalificerad")

    # ... eller ...

    tid = models.DecimalField("Tid", max_digits=3, decimal_places=2, null=True, blank=True)
    teknikfel = models.DecimalField("Fel", max_digits=3, decimal_places=0, null=True, blank=True)

    def disqualified(self):
        return self.diskvalificierad == True

    def fel(self):
        """Returnerar tidsfel, DISQUALIFIED eller None för fel, disk eller
inget resultat registrerat."""
        if self.disqualified():
            return self.RESULT_DISQUALIFIED

        elif self.tavling.reftid is None:
            return self.teknikfel

        else:
            return self.teknikfel + max(0, self.tid - self.tavling.reftid)


    def __unicode__(self):
        s = "%s och %s: " % (self.ekipage.forare, self.ekipage.hundnamn)
        if self.disqualified():
            s += "diskvalificerade"
        else:
            s += "%0.2fs, " % self.tid
            s += "%d fel" % self.fel()
        return s


    # Custom sort functions so I can easily sort and compare Result
    # objects.
    #
    ###########################
    # REMINDER: LESS IS MORE. #
    ###########################

    def __lt__(self, other):
        if other is None:
            return None

        a = SortableResult(self.fel(), self.tid, self.disqualified)
        b = SortableResult(other.fel(), other.tid, other.disqualified)
        return a < b

    def __le__(self, other):
        if other is None:
            return None

        a = SortableResult(self.fel(), self.tid, self.disqualified)
        b = SortableResult(other.fel(), other.tid, other.disqualified)
        return a <= b


    def __gt__(self, other):
        if other is None:
            return None

        a = SortableResult(self.fel(), self.tid, self.disqualified)
        b = SortableResult(other.fel(), other.tid, other.disqualified)
        return a > b

    def __ge__(self, other):
        if other is None:
            return None

        a = SortableResult(self.fel(), self.tid, self.disqualified)
        b = SortableResult(other.fel(), other.tid, other.disqualified)
        return a >= b

    def __eq__(self, other):
        if not other:
            return False

        a = SortableResult(self.fel(), self.tid, self.disqualified)
        b = SortableResult(other.fel(), other.tid, other.disqualified)
        return a == b

    def __ne__(self, other):
        return not self.__eq__(other)

# ----------------------------------------

class SortableResult:
    def __init__(self, faults, time, disq):
        self.faults = faults
        self.time = time
        self.disq = disq

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if self.faults is None:
            return "<Resultat: n/a>"
        return "<Resultat: %d fel, %0.2fs tid>" % (self.faults, self.time)

    def incomplete(self):
        return (self.faults is None and self.time is None) and not self.disqualified()

    def disqualified(self):
        return self.disq

    def __lt__(self, other):
        # Can't compare None
        if other is None:
            return None

        # All disqualifieds are equally bad, so we can't be better
        # than anyone if we're disqualified.
        if self.disqualified() and other.disqualified():
            return False

        if self.disqualified():
            return False

        if other.disqualified():
            return True

        # If we're incomplete, we're not better than the opposition -
        # just possibly equal to them.

        if self.incomplete() and other.incomplete():
            return False

        if self.incomplete():
            return False

        if other.incomplete():
            return True

        # We're neither disqualified or incomplete! Only compare times
        # if we have an equal amount of faults.

        if self.faults != other.faults:
            return self.faults < other.faults

        return self.time < other.time


    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        if self.__eq__(other) or self.__gt__(other):
            return True
        return False

    def __eq__(self, other):
        if other is None:
            return False

        if (self.disqualified() and other.disqualified()) or \
           (self.incomplete() and other.incomplete()):
            return True

        return self.faults == other.faults and self.time == other.time

    def __ne__(self, other):
        return not self.__eq__(other)


