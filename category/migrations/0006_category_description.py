# Generated by Django 4.2.16 on 2024-09-29 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_remove_category_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
