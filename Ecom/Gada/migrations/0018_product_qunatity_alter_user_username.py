# Generated by Django 4.2.2 on 2023-07-09 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gada', '0017_alter_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qunatity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
