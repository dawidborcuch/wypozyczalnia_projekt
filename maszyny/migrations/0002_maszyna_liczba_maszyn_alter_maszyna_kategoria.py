# Generated by Django 5.2.1 on 2025-05-14 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maszyny', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maszyna',
            name='liczba_maszyn',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='maszyna',
            name='kategoria',
            field=models.CharField(choices=[('budowlane', 'Maszyny budowlane'), ('ogrodnicze', 'Maszyny ogrodnicze'), ('przyczepki', 'Przyczepki')], max_length=20),
        ),
    ]
