from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse('index')


def result(request, word):
    return HttpResponse('searched word is %s' % word)


