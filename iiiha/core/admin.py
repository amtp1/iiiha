from django.contrib import admin

from .models import *


@admin.register(Assistant)
class Assistant(admin.ModelAdmin):
    fields = ['key_word', 'asst_id']
    list_display = ['key_word', 'asst_id']
    search_fields = ['key_word']


@admin.register(Tariff)
class Tariff(admin.ModelAdmin):
    fields = ['tariff_id', 'name']
    list_display = ['tariff_id', 'name']
    search_fields = ['tarrif_id', 'name']


@admin.register(TariffSet)
class TariffSet(admin.ModelAdmin):
    fields = ['user', 'tariff']
    list_display = ['user', 'tariff']
    search_fields = ['user', 'tariff']
