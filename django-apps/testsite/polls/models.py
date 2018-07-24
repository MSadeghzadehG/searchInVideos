from django.db import models

# Create your models here.


class Video(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class SerachResult(models.Model):
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    videoName = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.videoName.name + '/' + self.startTime + '-' + self.endTime


