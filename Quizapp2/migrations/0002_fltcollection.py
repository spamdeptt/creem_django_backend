# Generated by Django 4.1.3 on 2023-01-16 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizapp2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FLTCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tests', models.ManyToManyField(to='Quizapp2.quizquestioncollection')),
            ],
        ),
    ]