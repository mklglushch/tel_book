# Generated by Django 4.2.13 on 2024-08-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tel_book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
