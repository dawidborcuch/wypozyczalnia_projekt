from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Maszyna

def strona_glowna(request):
    maszyny = Maszyna.objects.all().order_by('nazwa')
    num_indicators = (maszyny.count() + 2) // 3  # Zaokrąglenie w górę
    
    # Liczniki maszyn dla każdej kategorii
    budowlane_count = Maszyna.objects.filter(kategoria='budowlane').count()
    ogrodnicze_count = Maszyna.objects.filter(kategoria='ogrodnicze').count()
    przyczepki_count = Maszyna.objects.filter(kategoria='przyczepki').count()
    
    return render(request, 'maszyny/strona_glowna.html', {
        'maszyny': maszyny,
        'num_indicators': num_indicators,
        'budowlane_count': budowlane_count,
        'ogrodnicze_count': ogrodnicze_count,
        'przyczepki_count': przyczepki_count
    })

def maszyny_budowlane(request):
    maszyny = Maszyna.objects.filter(kategoria='budowlane').order_by('nazwa')
    return render(request, 'maszyny/maszyny_lista.html', {
        'maszyny': maszyny,
        'tytul': 'Maszyny budowlane'
    })

def maszyny_ogrodnicze(request):
    maszyny = Maszyna.objects.filter(kategoria='ogrodnicze').order_by('nazwa')
    return render(request, 'maszyny/maszyny_lista.html', {
        'maszyny': maszyny,
        'tytul': 'Maszyny ogrodnicze'
    })

def przyczepki(request):
    maszyny = Maszyna.objects.filter(kategoria='przyczepki').order_by('nazwa')
    return render(request, 'maszyny/maszyny_lista.html', {
        'maszyny': maszyny,
        'tytul': 'Przyczepki'
    })

def cennik(request):
    maszyny = Maszyna.objects.all().order_by('kategoria', 'nazwa')
    return render(request, 'maszyny/cennik.html', {
        'maszyny': maszyny
    })

def kontakt(request):
    return render(request, 'maszyny/kontakt.html')

def o_nas(request):
    return render(request, 'maszyny/o_nas.html')

def maszyna_szczegoly(request, maszyna_id):
    maszyna = get_object_or_404(Maszyna, id=maszyna_id)
    return render(request, 'maszyny/maszyna_szczegoly.html', {
        'maszyna': maszyna
    })

def wyszukaj_maszyny(request):
    query = request.GET.get('q', '')
    if query:
        # Zamieniamy polskie znaki na ich odpowiedniki bez znaków diakrytycznych
        polskie_znaki = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        
        # Tworzymy wersję zapytania bez polskich znaków
        query_without_polish = query
        for polski, bez_polskiego in polskie_znaki.items():
            query_without_polish = query_without_polish.replace(polski, bez_polskiego)
        
        # Pobieramy wszystkie maszyny
        maszyny = Maszyna.objects.all()
        
        # Filtrujemy maszyny, które pasują do zapytania (z polskimi znakami lub bez)
        pasujace_maszyny = []
        for maszyna in maszyny:
            nazwa_bez_polskich = maszyna.nazwa
            for polski, bez_polskiego in polskie_znaki.items():
                nazwa_bez_polskich = nazwa_bez_polskich.replace(polski, bez_polskiego)
            
            if (query.lower() in maszyna.nazwa.lower() or 
                query_without_polish.lower() in nazwa_bez_polskich.lower()):
                pasujace_maszyny.append(maszyna)
                if len(pasujace_maszyny) >= 5:
                    break
        
        results = [{
            'id': maszyna.id,
            'nazwa': maszyna.nazwa,
            'kategoria': maszyna.get_kategoria_display(),
            'zdjecie': maszyna.zdjecie.url
        } for maszyna in pasujace_maszyny]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []}) 