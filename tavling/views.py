# -*- coding: utf-8 -*-
# Create your views here.
from tavling.models import *
from tavling.utils import sortfunc_object

from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('tavling/index.dtl')

def lag(request, storlek):
    lag = Team.objects.filter(size=storlek[0].upper()).order_by('order')
    lag = sorted(lag, key=sortfunc_object)
    return render_to_response('tavling/lag.dtl',
                              {'lag': lag,
                               'storlek': storlek})


def individuellt(request, storlek):
    deltagare = IndividualStart.objects.filter(size=storlek[0].upper())
    deltagare = sorted(deltagare, key=sortfunc_object)
    return render_to_response('tavling/individuellt.dtl',
                              {'deltagare': deltagare,
                               'storlek': storlek})
