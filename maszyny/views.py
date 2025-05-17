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
from .models import Maszyna
import locale
import re
from datetime import datetime, timedelta
from django.core.paginator import Paginator
import json
import logging
from django.utils.html import strip_tags

# Ustawienie locale na polskie
locale.setlocale(locale.LC_COLLATE, 'pl_PL.UTF-8')

# Cache timeout
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

logger = logging.getLogger(__name__)

def sort_with_polish_chars(maszyny):
    return sorted(maszyny, key=lambda x: locale.strxfrm(x.nazwa))

def get_cached_maszyny(category=None):
    cache_key = f'maszyny_{category}' if category else 'maszyny_all'
    maszyny = cache.get(cache_key)
    
    if maszyny is None:
        if category:
            maszyny = list(Maszyna.objects.filter(kategoria=category))
        else:
            maszyny = list(Maszyna.objects.all())
        maszyny = sort_with_polish_chars(maszyny)
        cache.set(cache_key, maszyny, CACHE_TTL)
    
    return maszyny

@csrf_protect
def index(request):
    maszyny = get_cached_maszyny()
    num_indicators = (len(maszyny) + 2) // 3
    
    # Liczniki maszyn dla każdej kategorii
    budowlane_count = cache.get('budowlane_count')
    if budowlane_count is None:
        budowlane_count = Maszyna.objects.filter(kategoria='budowlane').count()
        cache.set('budowlane_count', budowlane_count, CACHE_TTL)
    
    ogrodnicze_count = cache.get('ogrodnicze_count')
    if ogrodnicze_count is None:
        ogrodnicze_count = Maszyna.objects.filter(kategoria='ogrodnicze').count()
        cache.set('ogrodnicze_count', ogrodnicze_count, CACHE_TTL)
    
    przyczepki_count = cache.get('przyczepki_count')
    if przyczepki_count is None:
        przyczepki_count = Maszyna.objects.filter(kategoria='przyczepki').count()
        cache.set('przyczepki_count', przyczepki_count, CACHE_TTL)
    
    return render(request, 'maszyny/strona_glowna.html', {
        'maszyny': maszyny,
        'num_indicators': num_indicators,
        'budowlane_count': budowlane_count,
        'ogrodnicze_count': ogrodnicze_count,
        'przyczepki_count': przyczepki_count
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
    maszyny = get_cached_maszyny()
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