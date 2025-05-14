from django.db import models

class Maszyna(models.Model):
    KATEGORIE = [
        ('budowlane', 'Maszyny budowlane'),
        ('ogrodnicze', 'Maszyny ogrodnicze'),
        ('przyczepki', 'Przyczepki'),
    ]
    
    nazwa = models.CharField(max_length=200)
    opis = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    zdjecie = models.ImageField(upload_to='maszyny/')
    kategoria = models.CharField(max_length=20, choices=KATEGORIE)
    data_dodania = models.DateTimeField(auto_now_add=True)
    liczba_maszyn = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = 'Maszyny'
        ordering = ['-data_dodania']
    
    def __str__(self):
        return self.nazwa 