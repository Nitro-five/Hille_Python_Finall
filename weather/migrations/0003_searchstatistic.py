# Generated by Django 5.1.3 on 2025-01-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=100, unique=True)),
                ('search_count', models.IntegerField(default=0)),
            ],
        ),
    ]
