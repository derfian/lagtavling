# -*- coding: utf-8 -*-
from tavling.models import Tavling, Lag, Ekipage, Resultat, Laganmalan
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

class LagForm(forms.ModelForm):
    class Meta:
        model = Lag
    def clean(self):
        ekipage = self.cleaned_data.get('ekipage')
        if ekipage is not None and ekipage.count() > 4:
            raise ValidationError("För många deltagare i laget!")
        return self.cleaned_data

class LagAdmin(admin.ModelAdmin):
    form = LagForm

admin.site.register(Lag, LagAdmin)
admin.site.register(Tavling)
admin.site.register(Ekipage)
admin.site.register(Resultat)
admin.site.register(Laganmalan)
