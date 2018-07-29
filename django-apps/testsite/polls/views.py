from django.http import HttpResponse
from django.template import loader
from .models import Video
from .models import Subtitle
import datetime,webvtt

# Create your views here.


class PlaylistVideo:
    def __init__(self, video):
        self.video = video
        self.startTime = '00:00:00.000'
        self.endTime = '00:00:00.000'


def index(request, word):
    template = loader.get_template('index.html')
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')

    if word == 'null':
        videos_list = Video.objects.order_by('name')
    else:
        videos_list = search(word, subtitle_list)

    # for video in videos_list:
    #     if not (video.name in [video1.name for video1 in playlist]):
    #         playlist.append(video)
    context = {'playlist': videos_list, 'videos': videos_list, 'subtitles': subtitle_list, 'selectedVideo': videos_list[0]}
    return HttpResponse(template.render(context, request))


def search(word, subtitles):
    video_list = []
    print(datetime.datetime.now().time())
    for subtitle in subtitles:
        captions = webvtt.read(subtitle.get_file_name() + 'vtt')
        for caption in captions:
            # print(caption.text)
            if word in caption.text.lower():
                playlist_video = PlaylistVideo(subtitle.videoName)
                playlist_video.startTime = caption.start
                playlist_video.endTime = caption.end
                video_list.append(playlist_video)
    print(datetime.datetime.now().time())
    return video_list



