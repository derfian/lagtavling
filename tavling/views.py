# -*- coding: utf-8 -*-
# Create your views here.
from tavling.models import Tavling, Ekipage, Lag
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    tavlingar = Tavling.objects.all()
    for t in tavlingar:
        print "__", t
        print "____", t.deltagare()
    
    return render_to_response('tavling/index.dtl',
                              {'tavlingar': tavlingar})

def tavling(request, tavling_id):
    _tavling = get_object_or_404(Tavling, pk=tavling_id)
    return render_to_response('tavling/tavling_details.dtl',
                              {'tavling': _tavling,
                               'resultat': alla_deltagare(_tavling)})

def ekipage(request, ekipage_id):
    _ekipage = get_object_or_404(Ekipage, pk=ekipage_id)
    return render_to_response('tavling/ekipage_details.dtl',
                              {'ekipage': _ekipage})

def lag(request, lag_id):
    _lag = get_object_or_404(Lag, pk=lag_id)
    return render_to_response('tavling/lag_details.dtl',
                              {'lag': _lag})
