from django.db import models

# Create your models here.


class Video(models.Model):
    name = models.CharField(max_length=1000)
    videoFormat = models.CharField(max_length=200, default='video/mp4')
    videoQuality = models.CharField(max_length=200, default='576')
    videoPath = models.TextField(max_length=10000, default='https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-576p.mp4')

    def __str__(self):
        return self.name


class Subtitle(models.Model):
    videoName = models.ForeignKey(Video, on_delete=models.CASCADE)
    subtitlePath = models.TextField(max_length=10000, default='https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-HD.en.vtt')
    subtitleLanguage = models.CharField(max_length=200, default='en')

    def __str__(self):
        return self.videoName.name + ' ' + self.subtitleLanguage


