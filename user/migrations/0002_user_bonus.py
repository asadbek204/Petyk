# Generated by Django 5.0.4 on 2024-04-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonus',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
