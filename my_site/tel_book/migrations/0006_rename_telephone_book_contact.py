# Generated by Django 4.2.13 on 2024-10-18 19:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tel_book', '0005_rename_book_telephone_book'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Telephone_book',
            new_name='Contact',
        ),
    ]