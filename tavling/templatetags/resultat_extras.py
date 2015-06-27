# -*- coding: utf-8 -*-
from django import template
from tavling.utils import result_to_beat

register = template.Library()

@register.filter
def resultat(value, attrs="", borders=True, extra_classes=[]):
    if value is None:
        return '<td colspan="2" class="td-border-left td-border-right %s"></td>' % (' '.join(extra_classes))
    elif value[2]:
        return '<td colspan="2" class="text-center danger td-border-left td-border-right %s">Diskvalificerad</td>' % (' '.join(extra_classes))
    else:
        return '<td class="text-center td-border-left %s">%s</td><td class="text-center td-border-right %s">%0.2f</td>' % (' '.join(extra_classes),
                                                                                                                           value[0],
                                                                                                                           ' '.join(extra_classes),
                                                                                                                           value[1])


@register.filter
def resultat_att_sla(value, leader):
    return resultat(result_to_beat(leader, value), extra_classes=['shadow_result'])
