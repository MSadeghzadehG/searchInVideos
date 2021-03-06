# Generated by Django 2.0.5 on 2018-07-25 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20180723_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitlePath', models.FilePathField(default='polls/static/captions.vtt')),
                ('subtitleLanguage', models.CharField(default='en', max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='serachresult',
            name='videoName',
        ),
        migrations.AddField(
            model_name='video',
            name='videoFormat',
            field=models.CharField(default='video/mp4', max_length=200),
        ),
        migrations.AddField(
            model_name='video',
            name='videoPath',
            field=models.FilePathField(default='/polls/static/video.mp4'),
        ),
        migrations.AddField(
            model_name='video',
            name='videoQuality',
            field=models.CharField(default='480', max_length=200),
        ),
        migrations.DeleteModel(
            name='SerachResult',
        ),
        migrations.AddField(
            model_name='subtitle',
            name='videoName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Video'),
        ),
    ]
