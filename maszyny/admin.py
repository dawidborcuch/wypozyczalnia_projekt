from django.contrib import admin
from .models import Maszyna
 
@admin.register(Maszyna)
class MaszynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kategoria', 'cena', 'data_dodania')
    list_filter = ('kategoria',)
    search_fields = ('nazwa', 'opis') 