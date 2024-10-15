from django.contrib import admin

from .models import *

@admin.register(User)
class User(admin.ModelAdmin):
    pass

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
