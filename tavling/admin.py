# -*- coding: utf-8 -*-
#from tavling.models import Klass, Lag, Ekipage, Resultat, Laganmalan
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from tavling.models import Contestant, TeamMember, Result, Team, IndividualStart, ReferenceTime

#class ContestantInline(admin.TabularInline):
#    model = Contestant

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    max_num = 4
    extra = 4
    ordering = ('teamorder',)

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]
    list_filter = ('size',)
    list_display = ('size', 'order', 'name')
    ordering = ('size', 'order')

admin.site.register(Team, TeamAdmin)

class IndividualAdmin(admin.ModelAdmin):
    list_filter = ('size',)
    list_display = ('size', 'order', 'contestant', 'jumping_result', 'agility_result')
    ordering = ('size', 'order')
    list_editable = ('jumping_result', 'agility_result')
    
admin.site.register(IndividualStart, IndividualAdmin)


admin.site.register(ReferenceTime)

# Hide these from the regular admin interface - you're only supposed
# to edit them through teams and individual starts.

admin.site.register(Result)
admin.site.register(Contestant)
