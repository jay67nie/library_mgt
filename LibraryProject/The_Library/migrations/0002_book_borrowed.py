# Generated by Django 4.0.5 on 2022-06-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrowed',
            field=models.BooleanField(default=False),
        ),
    ]