# Generated by Django 3.2.8 on 2021-10-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcgplaya', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cart',
            field=models.ManyToManyField(to='tcgplaya.CardListing'),
        ),
    ]