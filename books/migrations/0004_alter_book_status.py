# Generated by Django 4.2.16 on 2024-09-30 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], default='Available', max_length=55),
        ),
    ]
