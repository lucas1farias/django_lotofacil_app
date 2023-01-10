

from django.contrib import admin
from .models import *


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('code', 'created', 'updated', 'availability')


@admin.register(NewGame)
class NewGameAdmin(admin.ModelAdmin):
    list_display = ('game_text', 'created', 'updated', 'availability')
