# Generated by Django 3.1.1 on 2021-04-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0002_auto_20210409_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
