# Generated by Django 4.1.3 on 2023-01-17 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quizapp2', '0012_alter_trendingarchive_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trendingarchive',
            options={'ordering': ['-updated_at'], 'verbose_name_plural': 'Trending Topics Archives'},
        ),
    ]
