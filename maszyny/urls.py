from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('maszyny-budowlane/', views.maszyny_budowlane, name='maszyny_budowlane'),
    path('maszyny-ogrodnicze/', views.maszyny_ogrodnicze, name='maszyny_ogrodnicze'),
    path('przyczepki/', views.przyczepki, name='przyczepki'),
    path('cennik/', views.cennik, name='cennik'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('o-nas/', views.o_nas, name='o_nas'),
    path('maszyna/<int:maszyna_id>/', views.maszyna_szczegoly, name='maszyna_szczegoly'),
    path('wyszukaj/', views.wyszukaj_maszyny, name='wyszukaj'),
    path('get-suggestions/', views.get_suggestions, name='get_suggestions'),
] 