# Generated by Django 5.0.4 on 2024-04-30 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_button_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='icon',
            field=models.ImageField(upload_to='button/'),
        ),
    ]
