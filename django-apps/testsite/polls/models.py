from django.db import models
from django.core import serializers
import webvtt,urllib.request,os
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# Create your models here.


class Video(models.Model):
    name = models.CharField(max_length=1000)
    videoFormat = models.CharField(max_length=200, default='video/mp4')
    videoQuality = models.CharField(max_length=200, default='576')
    videoPath = models.TextField(max_length=10000, default='https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-576p.mp4')

    def __str__(self):
        return self.name

    def get_serializble(self):
        return serializers.serialize("json", [self, ])


# def file_get_contents(subtitle):

class Subtitle(models.Model):
    videoName = models.ForeignKey(Video, on_delete=models.CASCADE)
    subtitlePath = models.TextField(max_length=10000, default='https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-HD.en.vtt')
    subtitleFormat = models.CharField(max_length=100,default='vtt')
    subtitleLanguage = models.CharField(max_length=200, default='en')

    def __str__(self):
        return self.videoName.name + ' ' + self.subtitleLanguage

    def get_serializble(self):
        return serializers.serialize("json", [self, ])

    def get_file_name(self):
        return '/tmp/' + self.videoName.name + self.subtitleLanguage + '.'

    def file_get_contents(self):
        filename = self.get_file_name()
        f = open(filename + self.subtitleFormat, 'wb')

        val = URLValidator()
        try:
            val(self.subtitlePath)
            output = urllib.request.urlopen(self.subtitlePath).read()
        except ValidationError:
            # from django.contrib.staticfiles.storage import staticfiles_storage
            # with open(staticfiles_storage.url(filename)) as f:
            #     return f.read()
            pass

        f.write(output)
        f.close()

        if self.subtitleFormat == 'sbv':
            webvtt.from_sbv(filename + self.subtitleFormat
                            ).save(
                filename + 'vtt')
            print('sbv subtitle converted to vtt')
        elif self.subtitleFormat == 'srt':
            webvtt.from_srt(
                filename + self.subtitleFormat).save(
                filename + '.tt')
            print('srt subtitle converted to vtt')


# from .models import Subtitle
for subtitle in Subtitle.objects.order_by('subtitleLanguage'):
    # print(os.path.isfile(subtitle.get_file_name()+'vtt'))
    if not os.path.isfile(subtitle.get_file_name()+'vtt'):
        subtitle.file_get_contents()
