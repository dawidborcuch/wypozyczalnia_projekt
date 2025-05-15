from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
        maszyny = Maszyna.objects.filter(nazwa__icontains=query)[:5]
        results = [{
            'id': maszyna.id,
            'nazwa': maszyna.nazwa,
            'kategoria': maszyna.get_kategoria_display(),
            'zdjecie': maszyna.zdjecie.url
        } for maszyna in maszyny]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []}) 