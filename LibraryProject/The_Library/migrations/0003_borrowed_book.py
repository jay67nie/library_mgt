# Generated by Django 4.0.5 on 2022-06-18 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('The_Library', '0002_book_borrowed'),
    ]

    operations = [
        migrations.CreateModel(
            name='borrowed_book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returned', models.BooleanField()),
                ('student', models.CharField(max_length=100)),
                ('borrow_date', models.DateField()),
                ('return_date', models.DateField()),
                ('penalty_due', models.IntegerField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='The_Library.book')),
            ],
        ),
    ]