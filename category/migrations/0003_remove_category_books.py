# Generated by Django 4.2.16 on 2024-09-29 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='books',
        ),
    ]
