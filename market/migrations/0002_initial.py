# Generated by Django 5.0.4 on 2024-04-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='users',
            field=models.ManyToManyField(related_name='buttons', to='user.user'),
        ),
    ]
