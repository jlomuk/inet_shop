# Generated by Django 3.1.7 on 2021-04-07 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210407_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='qty',
            field=models.PositiveIntegerField(default=1, verbose_name='Кол-во'),
        ),
    ]