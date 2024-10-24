from django.contrib import admin

from .models import *

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['email']

@admin.register(Assistant)
class Assistant(admin.ModelAdmin):
    fields = ['key_word', 'asst_id']
    list_display = ['key_word', 'asst_id']
    search_fields = ['key_word']

@admin.register(Tariff)
class Tariff(admin.ModelAdmin):
    fields = ['tariff_id', 'name', 'price']
    list_display = ['tariff_id', 'name', 'price']
    search_fields = ['tarrif_id', 'name']

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    fields = ['payment_id', 'user', 'status', 'created', 'updated']
    list_display = ['payment_id', 'user', 'status']
    readonly_fields = ['payment_id', 'user', 'status', 'created', 'updated']

@admin.register(Service)
class Service(admin.ModelAdmin):
    fields = ['name', 'price']
    list_display = ['name', 'price']
    search_fields = ['name']
