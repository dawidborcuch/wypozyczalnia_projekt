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
        if not self.link_youtube:
            return None
        
        import re
        
        # Różne formaty URL YouTube:
        # https://www.youtube.com/watch?v=VIDEO_ID
        # https://youtu.be/VIDEO_ID
        # https://www.youtube.com/embed/VIDEO_ID
        # https://youtube.com/watch?v=VIDEO_ID&list=...
        # https://m.youtube.com/watch?v=VIDEO_ID
        
        video_id = None
        
        # Usuń białe znaki
        url = self.link_youtube.strip()
        
        # Różne wzorce dla różnych formatów URL YouTube
        patterns = [
            # youtu.be/VIDEO_ID
            r'youtu\.be\/([a-zA-Z0-9_-]{11})',
            # youtube.com/watch?v=VIDEO_ID lub youtube.com/embed/VIDEO_ID
            r'(?:youtube\.com\/(?:watch\?v=|embed\/))([a-zA-Z0-9_-]{11})',
            # youtube.com/watch?.*v=VIDEO_ID (z dodatkowymi parametrami)
            r'youtube\.com\/watch\?.*[&?]v=([a-zA-Z0-9_-]{11})',
            # m.youtube.com/watch?v=VIDEO_ID
            r'm\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if video_id and len(video_id) == 11:
            # Zwróć embed URL z parametrami dla lepszej kompatybilności
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&enablejsapi=1'
        
        return None 

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść")
    is_active = models.BooleanField(default=True, verbose_name="Aktywny")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        verbose_name = "Komunikat"
        verbose_name_plural = "Komunikaty"
        ordering = ['-created_at']

    def __str__(self):
        return self.title 