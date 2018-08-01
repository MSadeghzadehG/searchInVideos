from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from .models import Video
from .models import Subtitle
import datetime,webvtt,json

# Create your views here.


class PlaylistVideo:
    def __init__(self, video, subtitle, id):
        self.video = video
        self.subtitle = subtitle
        self.startTime = '00:00:00.000'
        self.endTime = '00:00:00.000'
        self.id = id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def ajax(request, word, time):
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')
    if word == 'null':
        videos_list = Video.objects.order_by('name')
    else:
        videos_list = search(word, subtitle_list, time)
    print(json.dump(videos_list, cls=MyEncoder))
    return HttpResponse(json.dumps(videos_list, cls=MyEncoder), content_type="application/json")


def index(request, word, time):
    template = loader.get_template('index.html')
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')

    if word == 'null':
        videos_list = Video.objects.order_by('name')
    else:
        videos_list = search(word, subtitle_list, time)

    # for video in videos_list:
    #     if not (video.name in [video1.name for video1 in playlist]):
    #         playlist.append(video)
    context = {'playlist': videos_list, 'videos': videos_list, 'subtitles': subtitle_list, 'selectedVideo': videos_list[0]}
    return HttpResponse(template.render(context, request))


def index1(request):
    template = loader.get_template('index1.html')
    context = {}
    print('index1')
    return HttpResponse(template.render(context, request))


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def search(word, subtitles, time):
    video_list = []
    results_num = 0
    # print(datetime.datetime.now().time())
    for subtitle in subtitles:
        captions = webvtt.read(subtitle.get_file_name() + 'vtt')
        for caption in captions:
            # print(caption.text)
            if word in caption.text.lower():
                #create edited subtitle and pass
                playlist_video = PlaylistVideo(subtitle.videoName.get_serializble(), subtitle.get_serializble(), results_num)
                results_num = results_num + 1
                if get_sec(caption.start.split('.')[0]) - time >= 0:
                    playlist_video.startTime = humanize_time(get_sec(caption.start.split('.')[0]) - time)
                else:
                    playlist_video.startTime = humanize_time(0)
                playlist_video.endTime = humanize_time(get_sec(caption.end.split('.')[0]) + time)
                video_list.append(playlist_video)
    # print(datetime.datetime.now().time())
    return video_list



