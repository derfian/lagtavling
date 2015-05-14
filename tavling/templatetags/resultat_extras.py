# -*- coding: utf-8 -*-
from django import template
from tavling.models import Resultat

register = template.Library()

@register.filter
def resultat_tid(value):
    if value is None:
        return ""
    elif value == Resultat.RESULT_DISQUALIFIED:
        return "Diskvalificerad"
    else:
        return value

@register.filter
def resultat_fel(value):
    if value is None:
        return ""
    elif value == Resultat.RESULT_DISQUALIFIED:
        return "--"
    else:
        return value

@register.filter
def lagresultat_tid(value):
    if value is None:
        return "--"
    elif value == Resultat.RESULT_DISQUALIFIED:
        return "Diskvalificerad"
    else:
        return value

@register.filter
def lagresultat_fel(value):
    if value is None:
        return "--"
    elif value == Resultat.RESULT_DISQUALIFIED:
        return "Diskvalificerad"
    else:
        return value
