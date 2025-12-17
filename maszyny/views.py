from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Maszyna, Announcement
import locale
import re
from datetime import datetime, timedelta
from django.core.paginator import Paginator
import json
import logging
from django.utils.html import strip_tags

# Ustawienie locale na polskie
try:
    locale.setlocale(locale.LC_COLLATE, 'pl_PL.UTF-8')
except locale.Error:
    # Na części serwerów (np. Ubuntu bez doinstalowanych locale) ta wartość może nie istnieć.
    # W takim wypadku sortowanie będzie działać, ale bez reguł dla polskich znaków.
    pass

# Cache timeout
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

logger = logging.getLogger(__name__)

def polish_maszyna_word(count: int) -> str:
    """
    Poprawna odmiana dla "maszyna":
    - 1 -> "maszyna"
    - 2-4 (ale nie 12-14) -> "maszyny"
    - pozostałe (w tym 0) -> "maszyn"
    Przykłady: 0 maszyn, 1 maszyna, 2 maszyny, 4 maszyny, 5 maszyn, 12 maszyn, 14 maszyn, 22 maszyny.
    """
    try:
        n = abs(int(count))
    except (TypeError, ValueError):
        return "maszyn"

    if n == 1:
        return "maszyna"
    if (n % 10 in (2, 3, 4)) and (n % 100 not in (12, 13, 14)):
        return "maszyny"
    return "maszyn"

def sort_with_polish_chars(maszyny):
    return sorted(maszyny, key=lambda x: locale.strxfrm(x.nazwa))

def get_maszyny(category=None):
    """
    Celowo BEZ cache:
    - na produkcji cache typu LocMemCache nie jest współdzielony między procesami gunicorna,
      więc potrafi dawać "losowo" nieaktualne liczniki/listy po dodaniu maszyny w adminie.
    - priorytetem jest aktualność danych (np. po dodaniu nowej maszyny).
    """
    if category:
        maszyny = list(Maszyna.objects.filter(kategoria=category))
    else:
        maszyny = list(Maszyna.objects.all())
    return sort_with_polish_chars(maszyny)

def get_active_announcement():
    return Announcement.objects.filter(is_active=True).order_by('-created_at').first()

@csrf_protect
def index(request):
    maszyny = get_maszyny()
    num_indicators = (len(maszyny) + 2) // 3
    
    # Liczniki maszyn dla każdej kategorii
    budowlane_count = Maszyna.objects.filter(kategoria='budowlane').count()
    ogrodnicze_count = Maszyna.objects.filter(kategoria='ogrodnicze').count()
    przyczepki_count = Maszyna.objects.filter(kategoria='przyczepki').count()
    
    active_announcement = get_active_announcement()
    
    return render(request, 'maszyny/strona_glowna.html', {
        'maszyny': maszyny,
        'num_indicators': num_indicators,
        'budowlane_count': budowlane_count,
        'ogrodnicze_count': ogrodnicze_count,
        'przyczepki_count': przyczepki_count,
        'budowlane_word': polish_maszyna_word(budowlane_count),
        'ogrodnicze_word': polish_maszyna_word(ogrodnicze_count),
        'przyczepki_word': polish_maszyna_word(przyczepki_count),
        'active_announcement': active_announcement
    })

@csrf_protect
def maszyny_budowlane(request):
    try:
        maszyny = Maszyna.objects.filter(kategoria='budowlane')
        sort_by = request.GET.get('sort', 'nazwa_asc')
        
        if sort_by == 'cena_asc':
            maszyny = maszyny.order_by('cena')
        elif sort_by == 'cena_desc':
            maszyny = maszyny.order_by('-cena')
        elif sort_by == 'nazwa_asc':
            maszyny = sort_with_polish_chars(maszyny)
        elif sort_by == 'nazwa_desc':
            maszyny = sorted(maszyny, key=lambda x: locale.strxfrm(x.nazwa), reverse=True)
        else:
            maszyny = sort_with_polish_chars(maszyny)
        
        return render(request, 'maszyny/maszyny_lista.html', {
            'maszyny': maszyny,
            'tytul': 'Maszyny budowlane'
        })
    except Exception as e:
        logger.error(f"Błąd w widoku maszyny_budowlane: {str(e)}")
        return render(request, 'maszyny/error.html', {'error': 'Wystąpił błąd podczas ładowania strony.'}, status=500)

@csrf_protect
def maszyny_ogrodnicze(request):
    try:
        maszyny = Maszyna.objects.filter(kategoria='ogrodnicze')
        sort_by = request.GET.get('sort', 'nazwa_asc')
        
        if sort_by == 'cena_asc':
            maszyny = maszyny.order_by('cena')
        elif sort_by == 'cena_desc':
            maszyny = maszyny.order_by('-cena')
        elif sort_by == 'nazwa_asc':
            maszyny = sort_with_polish_chars(maszyny)
        elif sort_by == 'nazwa_desc':
            maszyny = sorted(maszyny, key=lambda x: locale.strxfrm(x.nazwa), reverse=True)
        else:
            maszyny = sort_with_polish_chars(maszyny)
        
        return render(request, 'maszyny/maszyny_lista.html', {
            'maszyny': maszyny,
            'tytul': 'Maszyny ogrodnicze'
        })
    except Exception as e:
        logger.error(f"Błąd w widoku maszyny_ogrodnicze: {str(e)}")
        return render(request, 'maszyny/error.html', {'error': 'Wystąpił błąd podczas ładowania strony.'}, status=500)

@csrf_protect
def przyczepki(request):
    try:
        maszyny = Maszyna.objects.filter(kategoria='przyczepki')
        sort_by = request.GET.get('sort', 'nazwa_asc')
        
        if sort_by == 'cena_asc':
            maszyny = maszyny.order_by('cena')
        elif sort_by == 'cena_desc':
            maszyny = maszyny.order_by('-cena')
        elif sort_by == 'nazwa_asc':
            maszyny = sort_with_polish_chars(maszyny)
        elif sort_by == 'nazwa_desc':
            maszyny = sorted(maszyny, key=lambda x: locale.strxfrm(x.nazwa), reverse=True)
        else:
            maszyny = sort_with_polish_chars(maszyny)
        
        return render(request, 'maszyny/maszyny_lista.html', {
            'maszyny': maszyny,
            'tytul': 'Przyczepki'
        })
    except Exception as e:
        logger.error(f"Błąd w widoku przyczepki: {str(e)}")
        return render(request, 'maszyny/error.html', {'error': 'Wystąpił błąd podczas ładowania strony.'}, status=500)

@csrf_protect
def cennik(request):
    maszyny = get_maszyny()
    return render(request, 'maszyny/cennik.html', {
        'maszyny': maszyny
    })

@csrf_protect
def kontakt(request):
    return render(request, 'maszyny/kontakt.html')

@csrf_protect
def o_nas(request):
    return render(request, 'maszyny/o_nas.html')

@csrf_protect
def maszyna_szczegoly(request, maszyna_id):
    try:
        maszyna = Maszyna.objects.get(id=maszyna_id)
        return render(request, 'maszyny/maszyna_szczegoly.html', {'maszyna': maszyna})
    except Maszyna.DoesNotExist:
        logger.warning(f"Próba dostępu do nieistniejącej maszyny o ID: {maszyna_id}")
        return render(request, 'maszyny/404.html', status=404)
    except Exception as e:
        logger.error(f"Błąd w widoku maszyna_szczegoly: {str(e)}")
        return render(request, 'maszyny/error.html', {'error': 'Wystąpił błąd podczas ładowania strony.'}, status=500)

def check_rate_limit(request):
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f'rate_limit_{ip}'
    requests = cache.get(cache_key, [])
    
    # Usuń stare zapytania (starsze niż 1 minuta)
    now = datetime.now()
    requests = [req for req in requests if now - req < timedelta(minutes=1)]
    
    if len(requests) >= 5:  # Limit 5 zapytań na minutę
        return False
    
    requests.append(now)
    cache.set(cache_key, requests, 60)  # Cache na 60 sekund
    return True

@csrf_protect
@require_http_methods(["GET"])
def wyszukaj_maszyny(request):
    try:
        if not check_rate_limit(request):
            return JsonResponse({
                'error': 'Przekroczono limit zapytań. Spróbuj ponownie za minutę.'
            }, status=429)
            
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return JsonResponse({
                'error': 'Zapytanie musi mieć co najmniej 2 znaki'
            }, status=400)
        
        # Walidacja zapytania
        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-]+$', query):
            return JsonResponse({
                'error': 'Zapytanie zawiera niedozwolone znaki'
            }, status=400)
        
        # Zamieniam polskie znaki na ich odpowiedniki bez znaków diakrytycznych
        polskie_znaki = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        
        # Wersja zapytania bez polskich znaków
        query_without_polish = query
        for polski, bez_polskiego in polskie_znaki.items():
            query_without_polish = query_without_polish.replace(polski, bez_polskiego)
        
        # Wyszukiwanie w nazwie i opisie
        maszyny = Maszyna.objects.filter(
            Q(nazwa__icontains=query) | 
            Q(opis__icontains=query)
        )
        
        # Sortowanie wyników według trafności
        results = []
        for maszyna in maszyny:
            score = 0
            if query.lower() in maszyna.nazwa.lower():
                score += 2
            if query.lower() in maszyna.opis.lower():
                score += 1
            results.append({
                'id': maszyna.id,
                'nazwa': strip_tags(maszyna.nazwa),
                'kategoria': maszyna.get_kategoria_display(),
                'cena': str(maszyna.cena),
                'zdjecie': maszyna.zdjecie.url if maszyna.zdjecie else None,
                'opis': strip_tags(maszyna.opis[:100] + '...' if len(maszyna.opis) > 100 else maszyna.opis),
                'score': score
            })
        
        # Sortowanie wyników
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return JsonResponse({'results': results[:5]})
    except Exception as e:
        logger.error(f"Błąd w widoku wyszukaj_maszyny: {str(e)}")
        return JsonResponse({'error': 'Wystąpił błąd podczas wyszukiwania.'}, status=400)

@require_http_methods(["GET"])
@csrf_protect
def get_suggestions(request):
    try:
        query = strip_tags(request.GET.get('query', '').strip())
        
        if not query:
            return JsonResponse({'suggestions': []})
        
        # Pobierz sugestie z cache
        cache_key = f'search_suggestions_{query}'
        suggestions = cache.get(cache_key)
        
        if not suggestions:
            # Wyszukaj maszyny pasujące do zapytania
            maszyny = Maszyna.objects.filter(
                Q(nazwa__icontains=query) | 
                Q(opis__icontains=query)
            ).values('nazwa', 'kategoria')[:5]
            
            suggestions = [
                {
                    'text': f"{strip_tags(m['nazwa'])} ({m['kategoria']})",
                    'value': strip_tags(m['nazwa'])
                }
                for m in maszyny
            ]
            
            # Zapisz sugestie w cache na 1 godzinę
            cache.set(cache_key, suggestions, 3600)
        
        return JsonResponse({'suggestions': suggestions})
    except Exception as e:
        logger.error(f"Błąd w widoku get_suggestions: {str(e)}")
        return JsonResponse({'error': 'Wystąpił błąd podczas pobierania sugestii.'}, status=400)

def rate_limit_view(request):
    """Widok wyświetlany po przekroczeniu limitu requestów."""
    return JsonResponse({
        'error': 'Przekroczono limit zapytań. Spróbuj ponownie później.'
    }, status=429) 