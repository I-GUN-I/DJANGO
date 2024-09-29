# Generated by Django 4.2.16 on 2024-09-27 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], max_length=55)),
                ('categories', models.ManyToManyField(to='category.category')),
            ],
        ),
    ]
