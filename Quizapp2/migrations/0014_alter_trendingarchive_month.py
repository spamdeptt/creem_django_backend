# Generated by Django 4.1.3 on 2023-01-17 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizapp2', '0013_alter_trendingarchive_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trendingarchive',
            name='month',
            field=models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=12),
        ),
    ]
