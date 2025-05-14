#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wypozyczalnia.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nie można zaimportować Django. Upewnij się, że jest zainstalowany i "
            "dostępny w zmiennej środowiskowej PYTHONPATH. Czy "
            "nie zapomniałeś aktywować środowiska wirtualnego? :)"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main() 