# Generated by Django 4.2.2 on 2023-06-28 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gada', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]