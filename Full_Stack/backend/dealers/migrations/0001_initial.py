# Generated by Django 5.0.3 on 2024-04-01 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('logo', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('rating_score', models.FloatField()),
                ('rating_count', models.IntegerField()),
                ('comments_count', models.IntegerField()),
                ('popularity', models.IntegerField()),
                ('city', models.IntegerField()),
            ],
        ),
    ]