# Generated by Django 3.2.8 on 2021-10-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcgplaya', '0003_auto_20211019_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='lang',
            field=models.CharField(default='', max_length=20),
        ),
    ]
