# -*- coding: utf-8 -*-
from django.db import models, connection
from tavling.utils import add_results, combine_results

SIZES = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))
KLASS = (('A', 'Agility'), ('J', 'Hopp'))
TEAMORDER = (('A', 'A'),
             ('B', 'B'),
             ('C', 'C'),
             ('D', 'D'))

TYPE = (('L', 'Lag'),
        ('I', 'Individuellt'))

# This can't be moved to utils or we'll create a circular dependency
# on ReferenceTime.
def get_result(res, size, type, klass):
    if res is None:
        return None
    if res.disqualified:
        return (0, 0, True)
    penalties = res.penalties
    try:
        ref = ReferenceTime.objects.get(size=size, type=type, klass=klass).reference
        penalties += max(0, res.time-ref)
    except:
        pass
    return (penalties, res.time, False)


class Contestant(models.Model):
    dog = models.CharField('Hund', max_length=100)
    handler = models.CharField('Förare', max_length=100)

    def __unicode__(self):
        return "%s och %s" % (self.handler, self.dog)

    class Meta:
        verbose_name = 'Ekipage'

class Result(models.Model):
    time = models.DecimalField('Tid', max_digits=5, decimal_places=2, null=True, blank=True)
    penalties = models.PositiveIntegerField('Fel (utan tidsfel)', null=True, blank=True, default=0)
    disqualified = models.BooleanField('Diskvalificerad')

    def __unicode__(self):
        if self.disqualified:
            return "disk."
        else:
            return "%d fel, %0.2fs" % (self.penalties, self.time)

    class Meta:
        verbose_name = 'Resultat'

class ReferenceTime(models.Model):
    size = models.CharField('Storlek', choices=SIZES, max_length=1)
    klass = models.CharField('Klass', choices=KLASS, max_length=1)
    type = models.CharField('Typ', choices=TYPE, max_length=1)
    reference = models.DecimalField('Referenstid', max_digits=5, decimal_places=2)

    def __unicode__(self):
        return "%s %s %s" % (self.size, self.klass, self.type)

    class Meta:
        unique_together = (('size','klass','type'),)


class Team(models.Model):
    size = models.CharField('Storlek', choices=SIZES, max_length=1)
    name = models.CharField('Lagnamn', max_length=100, unique=True)
    order = models.PositiveIntegerField('Startordning')

    class Meta:
        verbose_name = "LAG"

    def __unicode__(self):
        return "%s %d: %s" % (self.size, self.order, self.name)

    def hoppresultat(self):
        return combine_results([m.hoppresultat() for m in self.members.all()])

    def agilityresultat(self):
        return combine_results([m.agilityresultat() for m in self.members.all()])

    def aggregate(self):
        return add_results(self.hoppresultat(),
                           self.agilityresultat())

    def disqualified(self):
        a = self.aggregate()
        if a:
            return a[2]
        else:
            return False

    class Meta:
        unique_together = (('order', 'size'),)


class TeamMember(models.Model):
    class Meta:
        unique_together = (('team', 'teamorder'),)  # A team can't share teamorder with other teams
        verbose_name = "Lagmedlem"

    team = models.ForeignKey(Team, related_name='members')
    contestant = models.ForeignKey(Contestant, related_name='+', unique=True)
    teamorder = models.CharField('Lagordning', choices=TEAMORDER, max_length=1)

    jumping_result = models.ForeignKey(Result, related_name='+',
                                       null=True,
                                       blank=True,
                                       default=None)

    agility_result = models.ForeignKey(Result, related_name='+',
                                       null=True,
                                       blank=True,
                                       default=None)

    def hoppresultat(self):
        return get_result(self.jumping_result, self.team.size, 'L', 'J')

    def agilityresultat(self):
        return get_result(self.agility_result, self.team.size, 'L', 'A')

class IndividualStart(models.Model):
    class Meta:
        unique_together = (('order', 'size'),)
        verbose_name = "INDIVIDUELL START"

    # You can only compete once per handler/dog combination.
    contestant = models.ForeignKey(Contestant, unique=True)
    order = models.PositiveIntegerField('Startordning')
    size = models.CharField('Storlek', choices=SIZES, max_length=1)

    jumping_result = models.ForeignKey(Result, related_name='+',
                                       null=True,
                                       blank=True,
                                       default=None)

    agility_result = models.ForeignKey(Result, related_name='+',
                                       null=True,
                                       blank=True,
                                       default=None)

    def hoppresultat(self):
        return get_result(self.jumping_result, self.size, 'I', 'J')

    def agilityresultat(self):
        return get_result(self.agility_result, self.size, 'I', 'A')

    def aggregate(self):
        return add_results(self.hoppresultat(),
                           self.agilityresultat())

    def disqualified(self):
        a = self.aggregate()
        if a:
            return a[2]
        else:
            return False

    def __unicode__(self):
        return "%s %d: %s" % (self.size, self.order, unicode(self.contestant))

