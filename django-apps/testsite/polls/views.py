from django.http import HttpResponse
from django.template import loader
from django.conf import settings
# from django.core import serializers
from .models import Video
from .models import Subtitle
import datetime,webvtt,json,os,math
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp
from django.views.decorators.csrf import csrf_exempt
from collections import namedtuple


# Create your views here.


class PlaylistVideo:
    def __init__(self, video, subtitle, id, word, time):
        self.time = time
        self.word = word
        self.video = video
        self.subtitle = subtitle
        self.startTime = '00:00:00.000'
        self.endTime = '00:00:00.000'
        self.id = id


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def to_dict(videos_list):
    output = {}
    for video in videos_list:
        inner_output = {}
        inner_output['id'] = video.id
        inner_output['startTime'] = video.startTime
        inner_output['endTime'] = video.endTime
        inner_output['time'] = video.time
        inner_output['word'] = video.word
        inner_output['subtitle'] = video.subtitle.get_serializble()
        inner_output['video'] = video.video.get_serializble()
        output['result-'+video.id] = inner_output
    # print(output)
    return output


def ajax(request, word, time):
    request.session.save()
    # print(request.session.session_key)
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')
    # if word == 'null':
    #     videos_list = Video.objects.order_by('name')
    # else:
    videos_list = search(word, subtitle_list, time, request.session)
    # print(json.dumps(videos_list))
    return HttpResponse(json.dumps(to_dict(videos_list), cls=MyEncoder), content_type="application/json")


@csrf_exempt
def video_ajax(request):

    request.session.save()
    result_dir = '/media/result/' + str(request.session.session_key) + '/'

    data = request.body.decode('utf-8').split('[]')
    # print(data[0])
    # print('=============')
    # print(data[1])
    # print('=============')
    # print(data[2])
    # print('=============')
    p = json.loads(data[0], object_hook=lambda d: namedtuple('PlaylistVideo', d.keys())(*d.values()))
    s = json.loads(data[1], object_hook=lambda d: namedtuple('Subtitle', d.keys())(*d.values()))
    v = json.loads(data[2], object_hook=lambda d: namedtuple('Video', d.keys())(*d.values()))

    subtitle = Subtitle()
    subtitle.videoName = Video()
    subtitle.videoName.name = s.videoName
    subtitle.subtitleFormat = s.subtitleFormat
    subtitle.subtitleLanguage = s.subtitleLanguage
    subtitle.subtitlePath = s.subtitlePath

    video = Video()
    video.name = v.name
    video.videoPath = v.videoPath
    video.videoFormat = v.videoFormat
    video.videoQuality = v.videoQuality

    playlist_item = PlaylistVideo(video, subtitle, p.id, p.word, p.time)
    playlist_item.startTime = p.startTime
    playlist_item.endTime = p.endTime

    captions = webvtt.read(settings.MEDIA_ROOT + playlist_item.subtitle.get_file_name() + 'vtt')
    for caption in captions:
        if playlist_item.word in caption.text.lower():
            edited_sub = webvtt.WebVTT()
            for orginal_caption in captions:
                if get_sec(orginal_caption.start.split('.')[0]) >= get_sec(caption.start.split('.')[0]) - playlist_item.time and get_sec(
                        orginal_caption.end.split('.')[0]) <= get_sec(caption.end.split('.')[0]) + playlist_item.time:
                    edited_caption = orginal_caption.text.replace(playlist_item.word, '<u>' + playlist_item.word + '</u>')
                    edited_caption = edited_caption.replace(playlist_item.word.capitalize(), '<u>' + playlist_item.word.capitalize() + '</u>')
                    edited_sub.captions.append(webvtt.Caption(
                        humanize_time(
                            get_sec(orginal_caption.start.split('.')[0]) - get_sec(caption.start.split('.')[0]) + playlist_item.time) + '.' +
                        orginal_caption.start.split('.')[1],
                        humanize_time(
                            get_sec(orginal_caption.end.split('.')[0]) - get_sec(caption.start.split('.')[0]) + playlist_item.time) + '.' +
                        orginal_caption.end.split('.')[1],
                        [edited_caption]
                    ))
            edited_sub.save(
                settings.BASE_DIR + result_dir + playlist_item.word + '-' + str(playlist_item.id) + '-' + playlist_item.subtitle.get_file_name().split('/')[
                    1] + 'vtt')
    # print('subtitles saved')

    # print(playlist_item.subtitle.subtitlePath)
    # print(playlist_item.video.videoPath)

    for video1 in Video.objects.all():
        if video1.name == subtitle.videoName.name:
            sub_video = video1

    ffmpeg_extract_subclip(sub_video.videoPath, float(get_sec(playlist_item.startTime)),
                           float(get_sec(playlist_item.endTime)),
                           targetname=settings.BASE_DIR +
                                      result_dir + playlist_item.word +
                                      '-' + str(playlist_item.id) + '-' +
                                      playlist_item.subtitle.get_file_name().split('/')[1] +
                                      playlist_item.video.videoFormat.split('/')[1])
    # print('video created')

    return HttpResponse()


def index(request):
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


def get_duration(file):
    return math.floor(mp.VideoFileClip(file).duration)


def search(word, subtitles, time, session):
    video_list = []
    result_dir = '/media/result/' + str(session.session_key) + '/'
    # print(settings.BASE_DIR + result_dir)
    if not os.path.exists(settings.BASE_DIR + result_dir):
        os.makedirs(settings.BASE_DIR + result_dir)

    for subtitle in Subtitle.objects.order_by('subtitleLanguage'):
        if not os.path.isfile(settings.MEDIA_ROOT + subtitle.get_file_name() + 'vtt'):
            subtitle.file_get_contents()

    results_num = 0

    time1 = datetime.datetime.now().time()

    for subtitle in subtitles:
        captions = webvtt.read(settings.MEDIA_ROOT + subtitle.get_file_name() + 'vtt')

        for video in Video.objects.all():
            if video.name == subtitle.videoName.name:
                sub_video = video


        for caption in captions:

            if word in caption.text.lower():

                if get_sec(caption.start.split('.')[0]) - time >= 0:
                    startTime = humanize_time(get_sec(caption.start.split('.')[0]) - time)
                else:
                    startTime = humanize_time(0)
                if get_sec(caption.start.split('.')[0]) - time <= get_duration(sub_video.videoPath):
                    endTime = humanize_time(get_sec(caption.end.split('.')[0]) + time)
                else:
                    endTime = humanize_time(get_duration(sub_video))

                # ------create edited subtitle and pass-------

                s = Subtitle()
                s.subtitlePath = settings.SERVER_URL + result_dir + word + '-' + str(results_num) + '-' + subtitle.get_file_name().split('/')[1] + 'vtt'
                s.videoName = subtitle.videoName
                s.subtitleLanguage = subtitle.subtitleLanguage
                s.subtitleFormat = 'vtt'

                v = Video()
                v.videoFormat = sub_video.videoFormat
                v.videoQuality = sub_video.videoQuality
                v.videoPath = settings.SERVER_URL + result_dir + word + '-' + str(results_num) + '-' + subtitle.get_file_name().split('/')[1] + sub_video.videoFormat.split('/')[1]
                v.name = sub_video.name

                playlist_video = PlaylistVideo(v, s, str(results_num), word, time)
                playlist_video.startTime = startTime
                playlist_video.endTime = endTime

                video_list.append(playlist_video)
                results_num = results_num + 1

    time2 = datetime.datetime.now().time()
    print(time1)
    print(time2)
    return video_list
