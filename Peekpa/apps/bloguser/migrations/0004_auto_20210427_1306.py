# Generated by Django 2.2 on 2021-04-27 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloguser', '0003_auto_20210414_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyvisitnum',
            name='day',
            field=models.DateField(default='2021-04-27'),
        ),
        migrations.AlterField(
            model_name='uservisit',
            name='day',
            field=models.DateField(default='2021-04-27'),
        ),
    ]
