# Generated by Django 3.1.7 on 2021-04-06 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20210405_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_products',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
