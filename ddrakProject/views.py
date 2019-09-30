import calendar
import datetime
import random

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from schedule.models import Calendar, Event, Rule

######################################## global variables ########################################
UserModel = get_user_model()

slugs = ['DEFAULT', 'LFDM', 'MMGE', 'MYR']
admins = ['admin', '악의꽃admin', '막무간애admin', '모여락admin']
users = ['admin', '악의꽃', '막무간애', '모여락']
admin_slug_dict = {'admin':'DEFAULT', '악의꽃admin':'LFDM', '막무간애admin':'MMGE', '모여락admin':'MYR'}
user_slug_dict = {'admin':'DEFAULT', '악의꽃':'LFDM', '막무간애':'MMGE', '모여락':'MYR'}
slug_admin_dict = {'DEFAULT':'admin', 'LFDM':'악의꽃admin', 'MMGE':'막무간애admin', 'MYR':'모여락admin'}
slug_user_dict = {'DEFAULT':'admin', 'LFDM':'악의꽃', 'MMGE':'막무간애', 'MYR':'모여락'}

club_colors = ['dummy', '#1D60B9', '#E9567B', '#F08326']
color_set = ['#e53935', '#d81b60', '#8e24aa',
			 '#3949ab', '#1e88e5', '#039be5',
			 '#00acc1', '#00897b', '#43a047',
			 '#7cb342', '#827717', '#33691e',
			 '#ff6f00', '#e64a19', '#6d4c41'
			 ]
others_color = '#777777'
slug_color_dict = {'DEFAULT':'#000000', 'LFDM':'#1D60B9', 'MMGE':'#E9567B', 'MYR':'#F08326'}

################################### methods that DO NOT touch DB ##################################
'''
1. 간단한 유저 인증 절차 정도만 수행
2. html을 띄워주거나 url로 redirect 해주는 메서드들

Initialize             : 최초 페이지
change_password        : 비밀번호 변경 페이지
change_check           : 변경 결과 페이지
clubView               : 각 동아리별 시간표 페이지
SetTime                : admin계정으로 접속하는 월별 뜨락 시간 설정 페이지
StayAwake              : 철야 신청 페이지
IndividualTimeSet      : 동아리별 개인시간 설정 페이지
Borrow                 : 타 동아리 시간 대여 설정 페이지
'''
def Initialize(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/accounts/login/')
	else:
		return HttpResponseRedirect('/timetable')
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_result')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
        'user': request.user
    })

def change_check(request):
    return render_to_response('result.html')

def clubView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    user = request.user
    return render_to_response('clubTimetable.html', {'user': user, })

def SetTime(request):
    if (not request.user.is_authenticated or
        request.user.get_username() != 'admin'):
        return HttpResponseRedirect('/permission/')

    return render_to_response('SetTime.html')

def StayAwake(request):
    if (not request.user.is_authenticated or
        request.user.get_username() not in admins[1:]):
        return HttpResponseRedirect('/permission/')

    username = request.user.username
    return render_to_response('StayAwake.html', {'username': username,})

def IndividualTimeSet(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    username = request.user.username
    return render_to_response('IndividualTimeSet.html', {'username': username, })

def Borrow(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    username = request.user.username
    return render_to_response('Borrow.html', {'username': username, })

##################################### methods that DO touch DB ####################################
def filterAccount(eventSet, slug):
    # delete 메서드에서 사용
	for account in admins:
			if slug_admin_dict[slug] == account:
				continue
			else:
				eventSet = eventSet.exclude(creator=UserModel.objects.get(username=account))
	return eventSet

@csrf_exempt
def delete(request):
    title = request.POST.get('title')
    startStr = request.POST.get('start')
    endStr = request.POST.get('end')
    account = request.POST.get('username')
    start = datetime.datetime.strptime(startStr, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(endStr, '%Y-%m-%d %H:%M:%S')
    slug = admin_slug_dict[account]
	
    try:
        delete = Event.objects.get(title=title, start=start, end=end,)

        if delete.creator.username != account:
            return HttpResponseRedirect('/permission/')
        else:
            delete.delete()
			
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/permission/')
	
    except Event.MultipleObjectsReturned:
        eventSet = Event.objects.filter(title=title, start=start, end=end,)
        eventSet = filterAccount(eventSet, slug)
        eventSet.delete()
		
		
    if title == '철야':
        eventSet = Event.objects.filter(title=account[:-5], start=start, end=end,)
        eventSet = filterAccount(eventSet, slug)
        eventSet.delete()

    return HttpResponseRedirect('/clubTimetable/')

@csrf_exempt
def borrowSubmit(request):
    date = request.POST.getlist('date')
    time = request.POST.getlist('time')
    team = request.POST.get('teamname')
    club = request.POST.get('club')
    # Jul 13, 2018 12:30 PM
    start = datetime.datetime.strptime(date[0]+' '+time[0], '%b %d, %Y %I:%M %p')
    end = datetime.datetime.strptime(date[1]+' '+time[1], '%b %d, %Y %I:%M %p')
    color = random.choice(color_set)
    if end < start:
        url = '/BorrowError'
        return HttpResponseRedirect(url)

    url = '/timetable'
    if club in admins:
        url = '/clubTimetable'
		
    events = []
    
    for slug in slugs:
        if slug != 'DEFAULT':
            color = others_color
        events.append(Event(calendar=Calendar.objects.get(slug=slug),
                   			title=team,
                   			start=start,
                   			end=end,
                   			color_event=color,
                   			creator=UserModel.objects.get(username=club),)
					 )
		
    for event in events:	
        event.save()
    
    return HttpResponseRedirect(url)

@csrf_exempt
def clubSubmit(request):
    date = request.POST.getlist('date')
    time = request.POST.getlist('time')
    team = request.POST.get('teamname')
    club = request.POST.get('club')
    # example: Jul 13, 2018 12:30 PM
    start = datetime.datetime.strptime(date[0]+' '+time[0], '%b %d, %Y %I:%M %p')
    end = datetime.datetime.strptime(date[1]+' '+time[1], '%b %d, %Y %I:%M %p')
    color = random.choice(color_set)
    if end < start:
        url = '/ClubTimeError'
        return HttpResponseRedirect(url)

    url = '/timetable'
    
    if club in users or club in admins:
        if club in users:
            slug = user_slug_dict[club]
        else:
            slug = admin_slug_dict[club]
            
        event = Event(calendar=Calendar.objects.get(slug=slug),
                  title=team,
                  start=start,
                  end=end,
                  color_event = color,
                  creator=UserModel.objects.get(username=club),
                  )
        
        event.save()
        url = '/clubTimetable'

    return HttpResponseRedirect(url)

@csrf_exempt
def awakeSubmit(request):
    datestr = request.POST['date']
    club = request.POST['club']
    # 철야를 신청한 동아리의 calendar slug 값
    owner_slug = admin_slug_dict[club]
    color = slug_color_dict[owner_slug]

    start = (datetime.datetime.strptime(datestr, '%b %d, %Y') 
             + datetime.timedelta(days=1))
    end = start + datetime.timedelta(hours=6)

    try:
        event = Event.objects.get(calendar=Calendar.objects.get(slug='DEFAULT'),
                                  start=start,
                                  end=end,
                                  creator=UserModel.objects.get(username=club),
                                  )
        return HttpResponseRedirect('/StayAwakeError/')

    except ObjectDoesNotExist:
        event = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                      title=club[:-5],
                      start=start,
                      end=end,
                      color_event = color,
                      creator=UserModel.objects.get(username=club),
                      )
        event.save()
    
    # DEFAULT 제외
    for slug in slugs[1:]:
        if slug == owner_slug:
            title = '철야'
            c = '#AAAAAA'
        else:
            title = club[:-5]
            c = others_color
        
        Event(calendar=Calendar.objects.get(slug=slug),
              title=title,
              start=start,
              end=end,
              color_event=c,
              creator=UserModel.objects.get(username=club),
             ).save()
    
    url = '/timetable'
    return HttpResponseRedirect(url)

@csrf_exempt
def submit(request):
    morList = [
        request.POST.get('monMor'),
        request.POST.get('tueMor'),
        request.POST.get('wedMor'),
        request.POST.get('thuMor'),
        request.POST.get('friMor'),
        request.POST.get('satMor'),
        request.POST.get('sunMor'),
        ]
    aftList = [
        request.POST.get('monAft'),
        request.POST.get('tueAft'),
        request.POST.get('wedAft'),
        request.POST.get('thuAft'),
        request.POST.get('friAft'),
        request.POST.get('satAft'),
        request.POST.get('sunAft'),
        ]
    eveList = [
        request.POST.get('monEve'),
        request.POST.get('tueEve'),
        request.POST.get('wedEve'),
        request.POST.get('thuEve'),
        request.POST.get('friEve'),
        request.POST.get('satEve'),
        request.POST.get('sunEve'),
        ]
    weekList = [morList, aftList, eveList]
    month = request.POST.get('month')
    if month=='cur':
        curYear = datetime.date.today().year
        curMonth = datetime.date.today().month
    else:
        curMonth = datetime.date.today().month+1
        if curMonth==13:
            curMonth = 1
            curYear = datetime.date.today().year + 1
        else:
            curYear = datetime.date.today().year
            
    weekday = {'first':datetime.date(curYear, curMonth, 1).weekday(), 
               'last':datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()}
    firstWeekDay = datetime.date(curYear, curMonth, 1).weekday()
    firstDay = 1
    lastWeekDay = datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()
    lastDay = calendar.monthrange(curYear, curMonth)[1]

    setTime(weekList, weekday, curYear, curMonth, lastDay)

    url = '/timetable'
    return HttpResponseRedirect(url)

def getFLDay(i, weekday, lastDay):
    firstDay = 1
    days = {'first':1, 'last':31}
    if i < weekday['first']:
        days['first'] = firstDay - (weekday['first']-i) + 7
    else:
        days['first'] = firstDay + (i-weekday['first'])
    if i > weekday['last']:
        days['last'] = lastDay + (i-weekday['last']) - 7
    else:
        days['last'] = lastDay - (weekday['last']-i)
    
    return days

def setTime(weekList, weekday, curYear, curMonth, lastDay):
    j=1
    for aList in weekList:
        i=0
        isMorning = weekList.index(aList) == 0
        for day in aList:
            if isMorning:
                tit = tit = '오전 공용시간\n드럼/합주 우선:\n' + slug_user_dict[day]
                color = '#3d85c6'
            else:    
                tit = slug_user_dict[day]
                color = slug_color_dict[day]
            
            date = getFLDay(i, weekday, lastDay)
                
            for slug in slugs:
                # 해당 동아리 시간표에는 시간표를 비워둔다
                # 동아리 내 시간분배를 잘 볼 수 있게 하기 위함
                # 단, 아침은 예외
                if not isMorning and day == slug:
                    continue
                    
                if slug == 'DEFAULT':
                    c = slug_color_dict[day]
                else:
                    c = others_color
                    
                try:
                    event = Event.objects.get(calendar=Calendar.objects.get(slug=slug),
                                          start=datetime.datetime(curYear, curMonth, date['first'], j*6, 0),
                                          end=datetime.datetime(curYear, curMonth, date['first'], j*6, 0) + datetime.timedelta(hours=6),
                                          )
                    Event.objects.filter(calendar=Calendar.objects.get(slug=slug),
                                         start=datetime.datetime(curYear, curMonth, date['first'], j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, date['first'], j*6, 0) + datetime.timedelta(hours=6),
                                         ).update(title=tit, color_event=c, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    Event(calendar=Calendar.objects.get(slug=slug),
                          title=tit,
                          start=datetime.datetime(curYear, curMonth, date['first'], j*6, 0),
                          end=datetime.datetime(curYear, curMonth, date['first'], j*6, 0) + datetime.timedelta(hours=6),
                          rule=Rule.objects.get(id=3),  # Weekly;
                          end_recurring_period=datetime.datetime(curYear, curMonth, date['last'], j*6, 0) + datetime.timedelta(hours=6),
                          color_event=c,
                          creator=UserModel.objects.get(username='admin'),
                          ).save()
                
                # 이전에 설정을 했을 경우
                # 이미 등록되있는 다른 동아리 시간 삭제
                try:
                    Event.objects.get(calendar=Calendar.objects.get(slug=day),
                                      start=datetime.datetime(curYear, curMonth, date['first'], j*6, 0),
                                      end=datetime.datetime(curYear, curMonth, date['first'], j*6, 0) + datetime.timedelta(hours=6),
                                      ).delete()
                except ObjectDoesNotExist:
                    pass

            i += 1
        j += 1
    
    return
