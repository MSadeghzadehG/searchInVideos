# Generated by Django 2.0.5 on 2018-07-23 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serachresult',
            name='endTime',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='serachresult',
            name='startTime',
            field=models.CharField(max_length=200),
        ),
    ]
