# Generated by Django 2.1 on 2023-08-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20230813_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='blob',
            field=models.ImageField(upload_to='onestop/grocery/inventory/'),
        ),
    ]
