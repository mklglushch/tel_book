# Generated by Django 5.1.2 on 2024-11-13 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tel_book', '0006_rename_telephone_book_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='is_private',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]