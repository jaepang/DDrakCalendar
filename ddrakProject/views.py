from django.views import generic
from django.shortcuts import render_to_response, HttpResponse
from schedule.models import Calendar, Event, Rule
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import datetime
import calendar

def LFDM(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '악의꽃' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')
    
    return render_to_response('LFDMtimetable.html')


def MMGE(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '막무간애' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    return render_to_response('MMGEtimetable.html')
    

def MYR(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '모여락' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    return render_to_response('MYRtimetable.html')

def SetTime(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    return render_to_response('SetTime.html')

# morning submit
@csrf_exempt
def submit1(request):
    morList = [
        request.POST.getlist('monMor'),
        request.POST.getlist('tueMor'),
        request.POST.getlist('wedMor'),
        request.POST.getlist('thuMor'),
        request.POST.getlist('friMor'),
        request.POST.getlist('satMor'),
        request.POST.getlist('sunMor'),
    ]
    for day in morList:
        if day == 'LFDM':
            tit = '악의꽃'
        elif day == 'MMGE':
            tit = '막무간애'
        elif day == 'MYR':
            tit = '모여락'
        event = Event(Calendar=Calendar.objects.get(slug='DEFAULT'),
                      title=tit,
                      start=datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1, 6, 00),
                      end=datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1, 12, 00),
                      rule=Rule.objects.get(id=3),
                      end_recurring_period=datetime.datetime(datetime.date.today().year, datetime.date.today().month, calendar.monthrange(datetime.date.today().year, date.datetime.today().month)[1], 12, 00),
                      )
        event.save()

    url = '/submit2'
    return HttpResponseRedirect(url)


@csrf_exempt
def submit2(request):
    aftList = [
        request.POST.getlist('monAft'),
        request.POST.getlist('tueAft'),
        request.POST.getlist('wedAft'),
        request.POST.getlist('thuAft'),
        request.POST.getlist('friAft'),
        request.POST.getlist('satAft'),
        request.POST.getlist('sunAft'),
    ]
    print(aftList)
    for day in aftList:
        if day == 'LFDM':
            tit = '악의꽃'
        elif day == 'MMGE':
            tit = '막무간애'
        elif day == 'MYR':
            tit = '모여락'
        event = Event(Calendar=Calendar.objects.get(slug='DEFAULT'),
                      title=tit,
                      start=datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1, 12, 00),
                      end=datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1, 18, 00),
                      rule=Rule.objects.get(id=3),
                      end_recurring_period=datetime.datetime(datetime.date.today().year, datetime.date.today().month, calendar.monthrange(datetime.date.today().year, date.datetime.today().month)[1], 18, 00),
                      )
        event.save()
    
    url = '/submit3'
    return HttpResponseRedirect(url)

@csrf_exempt
def submit3(request):
    eveList = [
        request.POST['monEve'],
        request.POST['tueEve'],
        request.POST['wedEve'],
        request.POST['thuEve'],
        request.POST['friEve'],
        request.POST['satEve'],
        request.POST['sunEve'],
    ]
    # print(eveList)
    curYear = datetime.date.today().year
    curMonth = datetime.date.today().month
    firstWeekDay = datetime.date(curYear, curMonth, 1).weekday()
    firstDay = 1
    lastWeekDay = datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()
    lastDay = calendar.monthrange(curYear, curMonth)[1]
    i = 0
    for day in eveList:
        if day == 'LFDM':
            tit = '악의꽃'
            color = '#1D60B9'
            flag = 1
        elif day == 'MMGE':
            tit = '막무간애'
            color = '#E9567B'
            flag = 2
        elif day == 'MYR':
            tit = '모여락'
            color = '#F08326'
            flag = 3
        if i < firstWeekDay:
            fday = firstDay - (firstWeekDay-i) + 7
        else:
            fday = firstDay + (i-firstWeekDay)
        if i > lastWeekDay:
            lday = lastDay + (i-lastWeekDay) - 7
        else:
            lday = lastDay - (lastWeekDay-i)
        print(fday, lday)
        event = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                      title=tit,
                      start=datetime.datetime(curYear, curMonth, fday, 18, 0),
                      end=datetime.datetime(curYear, curMonth, fday, 23, 59),
                      rule=Rule.objects.get(id=3), # Weekly;
                      end_recurring_period=datetime.datetime(curYear, curMonth, lday, 23, 59),
                      color_event = color,
                      )
        event.save()

        # 악꽃 시간표를 막, 모에 전달
        if flag == 1:
            event1 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 18, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 23, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 23, 59),
                          color_event=color,
                          )
            event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 18, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 23, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 23, 59),
                          color_event=color,
                          )
            event1.save()
            event2.save()

        # 막간 시간표를 악, 모에 전달
        elif flag == 2:
            event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                           title=tit,
                           start=datetime.datetime(curYear, curMonth, fday, 18, 0),
                           end=datetime.datetime(curYear, curMonth, fday, 23, 59),
                           rule=Rule.objects.get(id=3),  # Weekly;
                           end_recurring_period=datetime.datetime(curYear, curMonth, lday, 23, 59),
                           color_event=color,
                           )
            event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                           title=tit,
                           start=datetime.datetime(curYear, curMonth, fday, 18, 0),
                           end=datetime.datetime(curYear, curMonth, fday, 23, 59),
                           rule=Rule.objects.get(id=3),  # Weekly;
                           end_recurring_period=datetime.datetime(curYear, curMonth, lday, 23, 59),
                           color_event=color,
                           )
            event1.save()
            event2.save()

        # 모여락 시간표를 악, 막에 전달
        elif flag == 3:
            event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                           title=tit,
                           start=datetime.datetime(
                               curYear, curMonth, fday, 18, 0),
                           end=datetime.datetime(
                               curYear, curMonth, fday, 23, 59),
                           rule=Rule.objects.get(id=3),  # Weekly;
                           end_recurring_period=datetime.datetime(
                               curYear, curMonth, lday, 23, 59),
                           color_event=color,
                           )
            event2 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                           title=tit,
                           start=datetime.datetime(
                               curYear, curMonth, fday, 18, 0),
                           end=datetime.datetime(
                               curYear, curMonth, fday, 23, 59),
                           rule=Rule.objects.get(id=3),  # Weekly;
                           end_recurring_period=datetime.datetime(
                               curYear, curMonth, lday, 23, 59),
                           color_event=color,
                           )
            event1.save()
            event2.save()
        i += 1
        
    url = '/timetable'
    return HttpResponseRedirect(url)
