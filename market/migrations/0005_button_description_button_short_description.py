# Generated by Django 5.0.4 on 2024-04-30 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_alter_button_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='button',
            name='short_description',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
