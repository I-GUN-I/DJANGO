# Generated by Django 4.2.16 on 2024-09-29 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='categories',
        ),
    ]
