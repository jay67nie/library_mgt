# Generated by Django 4.0.5 on 2022-08-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Library', '0002_borrowed_book_notified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowed_book',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]