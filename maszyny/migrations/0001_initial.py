# Generated by Django 5.2.1 on 2025-05-13 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maszyna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200)),
                ('opis', models.TextField()),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zdjecie', models.ImageField(upload_to='maszyny/')),
                ('kategoria', models.CharField(choices=[('budowlane', 'Maszyny budowlane'), ('ogrodnicze', 'Maszyny ogrodnicze')], max_length=20)),
                ('data_dodania', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Maszyna',
                'verbose_name_plural': 'Maszyny',
                'ordering': ['-data_dodania'],
            },
        ),
    ]
