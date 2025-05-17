from django.db import models
from django.urls import reverse

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
    liczba_maszyn = models.IntegerField(default=1)
    link_youtube = models.URLField(max_length=200, blank=True, null=True, help_text="Link do filmu na YouTube")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = 'Maszyny'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nazwa 

    def get_absolute_url(self):
        return reverse('maszyna_szczegoly', args=[str(self.id)])

    def get_youtube_embed_url(self):
        if self.link_youtube:
            # Konwertuj URL YouTube na URL embed
            video_id = self.link_youtube.split('v=')[-1]
            return f'https://www.youtube.com/embed/{video_id}'
        return None 