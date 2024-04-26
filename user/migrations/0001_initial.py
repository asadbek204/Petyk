# Generated by Django 5.0.4 on 2024-04-22 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='')),
                ('user_id', models.PositiveBigIntegerField()),
                ('balance', models.PositiveBigIntegerField()),
                ('ref_link', models.CharField(max_length=256)),
                ('wallet_address', models.CharField(max_length=256)),
                ('energy', models.PositiveBigIntegerField()),
                ('energy_limit', models.PositiveBigIntegerField()),
                ('level', models.PositiveSmallIntegerField()),
                ('tap_step', models.PositiveSmallIntegerField()),
                ('refered_by', models.ManyToManyField(blank=True, null=True, related_name='friends', to='user.user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Harem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('balance', models.PositiveBigIntegerField(blank=True, default=0)),
                ('target', models.PositiveBigIntegerField()),
                ('members', models.ManyToManyField(related_name='harems', to='user.user')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='harem', to='user.user')),
            ],
            options={
                'verbose_name': 'harem',
                'verbose_name_plural': 'harems',
                'db_table': 'harems',
            },
        ),
    ]