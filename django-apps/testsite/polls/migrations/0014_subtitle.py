# Generated by Django 2.1 on 2018-08-02 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitlePath', models.TextField(default='https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-HD.en.vtt', max_length=10000)),
                ('subtitleFormat', models.CharField(default='vtt', max_length=100)),
                ('subtitleLanguage', models.CharField(default='en', max_length=200)),
                ('videoName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Video')),
            ],
        ),
    ]
