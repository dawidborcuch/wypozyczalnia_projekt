from django.contrib import admin
from .models import Maszyna
 
@admin.register(Maszyna)
class MaszynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kategoria', 'cena', 'created_at')
    list_filter = ('kategoria',)
    search_fields = ('nazwa', 'opis')
    ordering = ('-created_at',) 