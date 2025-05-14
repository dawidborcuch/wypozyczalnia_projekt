# Wypożyczalnia Maszyn

Aplikacja webowa do zarządzania wypożyczalnią maszyn budowlanych i ogrodniczych.

## Wymagania
- Python 3.8+
- pip (menedżer pakietów Pythona)

## Instalacja

1. Sklonuj repozytorium
2. Utwórz wirtualne środowisko:
```bash
python -m venv venv
```

3. Aktywuj wirtualne środowisko:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

5. Wykonaj migracje bazy danych:
```bash
python manage.py migrate
```

6. Utwórz superużytkownika (administratora):
```bash
python manage.py createsuperuser
```

## Uruchomienie

1. Uruchom serwer deweloperski:
```bash
python manage.py runserver
```

2. Otwórz przeglądarkę i przejdź pod adres: http://127.0.0.1:8000/

3. Panel administracyjny dostępny jest pod adresem: http://127.0.0.1:8000/admin/ 