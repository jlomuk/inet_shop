# Generated by Django 3.1.7 on 2021-04-01 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notebook',
            old_name='descriplion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='smartphone',
            old_name='descriplion',
            new_name='description',
        ),
    ]
