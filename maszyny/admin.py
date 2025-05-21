from django.contrib import admin
from .models import Maszyna, Announcement

@admin.register(Maszyna)
class MaszynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kategoria', 'cena', 'created_at')
    list_filter = ('kategoria',)
    search_fields = ('nazwa', 'opis')
    ordering = ('-created_at',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',) 