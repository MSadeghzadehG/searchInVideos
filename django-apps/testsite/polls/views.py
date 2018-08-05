from django.http import HttpResponse
from django.template import loader
from django.conf import settings
# from django.core import serializers
from .models import Video
from .models import Subtitle
import datetime,webvtt,json,os

# Create your views here.


class PlaylistVideo:
    def __init__(self, video, subtitle, id):
        self.video = video
        self.subtitle = subtitle
        self.startTime = '00:00:00.000'
        self.endTime = '00:00:00.000'
        self.id = id

    # def __dict__(self):
    #     output = {};


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def toDict(videos_list):
    output = {}
    for video in videos_list:
        inner_output = {}
        inner_output['id'] = video.id
        inner_output['startTime'] = video.startTime
        inner_output['endTime'] = video.endTime
        inner_output['subtitle'] = video.subtitle.get_serializble()
        inner_output['video'] = video.video.get_serializble()
        output['result-'+video.id] = inner_output
    # print(output)
    return output


def ajax(request, word, time):
    request.session.save()
    print(request.session.session_key)
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')
    # if word == 'null':
    #     videos_list = Video.objects.order_by('name')
    # else:
    videos_list = search(word, subtitle_list, time, request.session)
    # print(json.dumps(videos_list))
    return HttpResponse(json.dumps(toDict(videos_list), cls=MyEncoder), content_type="application/json")


def index(request, word, time):
    template = loader.get_template('index.html')
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')

    if word == 'null':
        videos_list = Video.objects.order_by('name')
    else:
        videos_list = search(word, subtitle_list, time)
    context = {'playlist': videos_list, 'videos': videos_list, 'subtitles': subtitle_list, 'selectedVideo': videos_list[0]}
    return HttpResponse(template.render(context, request))


def index1(request):
    template = loader.get_template('index1.html')
    context = {}
    # print('index1')
    return HttpResponse(template.render(context, request))


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def search(word, subtitles, time, session):
    video_list = []
    # print(session.session_key)
    result_dir = '/media/result/' + str(session.session_key) + '/'
    # print(settings.BASE_DIR + result_dir)
    if not os.path.exists(settings.BASE_DIR + result_dir):
        os.makedirs(settings.BASE_DIR + result_dir)
        # print('dir maked')
    results_num = 0
    # print(datetime.datetime.now().time())
    for subtitle in subtitles:
        print(settings.MEDIA_ROOT + subtitle.get_file_name() + 'vtt')
        captions = webvtt.read(settings.MEDIA_ROOT + subtitle.get_file_name() + 'vtt')
        edited_sub = webvtt.WebVTT()
        for caption in captions:
            # print(caption.text)
            if word in caption.text.lower():
                # ------create edited subtitle and pass-------
                edited_caption = ''
                for orginal_word in caption.text.split(' '):
                    if not orginal_word == word:
                        edited_caption += orginal_word + ' '
                    else:
                        # edited_caption += '<green>'+orginal_word+'<green> '
                        edited_caption += '<u>' + orginal_word + '</u> '
                        # print('omad :)')
                e = Subtitle()
                e.subtitlePath = 'http://localhost:8000' + result_dir + word + '-' + subtitle.get_file_name().split('/')[1] + 'vtt'
                e.videoName = subtitle.videoName
                e.subtitleLanguage = subtitle.subtitleLanguage
                e.subtitleFormat = 'vtt'
                playlist_video = PlaylistVideo(subtitle.videoName, e, str(results_num))
                results_num = results_num + 1
                if get_sec(caption.start.split('.')[0]) - time >= 0:
                    playlist_video.startTime = humanize_time(get_sec(caption.start.split('.')[0]) - time)
                else:
                    playlist_video.startTime = humanize_time(0)
                playlist_video.endTime = humanize_time(get_sec(caption.end.split('.')[0]) + time)
                video_list.append(playlist_video)
            else:
                edited_caption = caption.text
            edited_sub.captions.append(webvtt.Caption(
                caption.start,
                caption.end,
                [edited_caption]
            ))
        edited_sub.save(settings.BASE_DIR + result_dir + word + '-' + subtitle.get_file_name().split('/')[1] + 'vtt')
    # print(datetime.datetime.now().time())
    return video_list



