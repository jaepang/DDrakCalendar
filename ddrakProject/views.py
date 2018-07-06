from django.views import generic
from django.shortcuts import render_to_response, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def LFDM(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/timetable/')

    elif request.user.get_username() != '악의꽃' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/timetable/')
    
    return render_to_response('LFDMtimetable.html')


def MMGE(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/timetable/')

    elif request.user.get_username() != '막무간애' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/timetable/')

    return render_to_response('MMGEtimetable.html')
    

def MYR(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/timetable/')

    elif request.user.get_username() != '모여락' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/timetable/')

    return render_to_response('MYRtimetable.html')

def SetTime(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/timetable/')

    elif request.user.get_username() != 'admin':
        return HttpResponseRedirect('/timetable/')

    return render_to_response('SetTime.html')
