# Generated by Django 4.2.16 on 2024-09-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_categories'),
        ('category', '0003_remove_category_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='books',
            field=models.ManyToManyField(to='books.book'),
        ),
    ]
