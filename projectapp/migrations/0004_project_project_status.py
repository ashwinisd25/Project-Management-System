# Generated by Django 3.1.7 on 2021-04-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0003_auto_20210409_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.BooleanField(default=False),
        ),
    ]
