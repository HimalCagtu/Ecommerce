# Generated by Django 4.2.2 on 2023-06-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gada', '0006_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
