from django.contrib import admin

from .models import *


@admin.register(Assistants)
class Assistants(admin.ModelAdmin):
    fields = ['key_word', 'asst_id']
    list_display = ['key_word', 'asst_id']
