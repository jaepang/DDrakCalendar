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

def Initialize(request):
    return HttpResponseRedirect('/accounts/login/')

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

@csrf_exempt
def submit(request):
    morList = [
        request.POST['monMor'],
        request.POST['tueMor'],
        request.POST['wedMor'],
        request.POST['thuMor'],
        request.POST['friMor'],
        request.POST['satMor'],
        request.POST['sunMor'],
    ]    
    aftList = [
        request.POST['monAft'],
        request.POST['tueAft'],
        request.POST['wedAft'],
        request.POST['thuAft'],
        request.POST['friAft'],
        request.POST['satAft'],
        request.POST['sunAft'],
    ]
    eveList = [
        request.POST['monEve'],
        request.POST['tueEve'],
        request.POST['wedEve'],
        request.POST['thuEve'],
        request.POST['friEve'],
        request.POST['satEve'],
        request.POST['sunEve'],
    ]
    weekList = [aftList, eveList]
    # print(eveList)
    curYear = datetime.date.today().year
    curMonth = datetime.date.today().month
    firstWeekDay = datetime.date(curYear, curMonth, 1).weekday()
    firstDay = 1
    lastWeekDay = datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()
    lastDay = calendar.monthrange(curYear, curMonth)[1]
    j=2
    for aList in weekList:
        i=0
        for day in aList:
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
            event = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                        title=tit,
                        start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                        end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                        rule=Rule.objects.get(id=3), # Weekly;
                        end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                        color_event = color,
                        )
            event.save()

            # 악꽃 시간표를 막, 모에 전달
            if flag == 1:
                event1 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                            title=tit,
                            start=datetime.datetime(
                                curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(
                                curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(
                                curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                            title=tit,
                            start=datetime.datetime(
                                curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(
                                curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(
                                curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event1.save()
                event2.save()

            # 막간 시간표를 악, 모에 전달
            elif flag == 2:
                event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                            title=tit,
                            start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                            title=tit,
                            start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event1.save()
                event2.save()

            # 모여락 시간표를 악, 막에 전달
            elif flag == 3:
                event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                            title=tit,
                            start=datetime.datetime(
                                curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(
                                curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(
                                curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event2 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                            title=tit,
                            start=datetime.datetime(
                                curYear, curMonth, fday, j*6, 0),
                            end=datetime.datetime(
                                curYear, curMonth, fday, j*6+5, 59),
                            rule=Rule.objects.get(id=3),  # Weekly;
                            end_recurring_period=datetime.datetime(
                                curYear, curMonth, lday, j*6+5, 59),
                            color_event=color,
                            )
                event1.save()
                event2.save()
            i += 1
        j += 1

    # For morning
    i=0
    for day in morList:
            if day == 'LFDM':
                tit = '오전 공용시간\n드럼/합주 우선:\n악의꽃'
            elif day == 'MMGE':
                tit = '오전 공용시간\n드럼/합주 우선:\n막무간애'
            elif day == 'MYR':
                tit = '오전 공용시간\n드럼/합주 우선:\n모여락'
            if i < firstWeekDay:
                fday = firstDay - (firstWeekDay-i) + 7
            else:
                fday = firstDay + (i-firstWeekDay)
            if i > lastWeekDay:
                lday = lastDay + (i-lastWeekDay) - 7
            else:
                lday = lastDay - (lastWeekDay-i)
            event1 = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 6, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 11, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 11, 59),
                          )
            event2 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 6, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 11, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 11, 59),
                          )
            event3 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 6, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 11, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 11, 59),
                          )
            event4 = Event(calendar=Calendar.objects.get(slug='MYR'),
                          title=tit,
                          start=datetime.datetime(
                              curYear, curMonth, fday, 6, 0),
                          end=datetime.datetime(
                              curYear, curMonth, fday, 11, 59),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(
                              curYear, curMonth, lday, 11, 59),
                          )
            event1.save()
            event2.save()
            event3.save()
            event4.save()
            i += 1
    
    url = '/timetable'
    return HttpResponseRedirect(url)
