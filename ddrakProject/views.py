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
'''
admin : 각 동아리의 관리자 계정 (회장 or 뜨락지기용)
user  : 각 동아리의 일반사용자 계정
slug  : 뜨락 전체 시간표(DEFAULT) 및 각 동아리 시간표 id 값

동아리 및 slug index (모든 list, dictionary에 적용할 것)
0: DEFAULT   (모든 동아리가 공유하는 부분이거나 공용 시간을 의미)
1: 악의꽃     (LFDM)
2: 막무간애   (MMGE)
3: 모여락     (MYR)
'''
UserModel = get_user_model()

slugs = ['DEFAULT', 'LFDM', 'MMGE', 'MYR']
admins = ['admin', '악의꽃admin', '막무간애admin', '모여락admin']
users = ['admin', '악의꽃', '막무간애', '모여락']
admin_slug_dict = {'admin':'DEFAULT', '악의꽃admin':'LFDM', '막무간애admin':'MMGE', '모여락admin':'MYR'}
user_slug_dict = {'admin':'DEFAULT', '악의꽃':'LFDM', '막무간애':'MMGE', '모여락':'MYR'}
slug_admin_dict = {'DEFAULT':'admin', 'LFDM':'악의꽃admin', 'MMGE':'막무간애admin', 'MYR':'모여락admin'}
slug_user_dict = {'DEFAULT':'admin', 'LFDM':'악의꽃', 'MMGE':'막무간애', 'MYR':'모여락'}

club_colors = ['#3a87ad', '#1D60B9', '#E9567B', '#F08326']
# 동아리 내 일정 or 대여해줄 때 다음 색 중 랜덤한 색으로 정해진다.
color_set = ['#e53935', '#d81b60', '#8e24aa',
			 '#3949ab', '#1e88e5', '#039be5',
			 '#00acc1', '#00897b', '#43a047',
			 '#7cb342', '#827717', '#33691e',
			 '#ff6f00', '#e64a19', '#6d4c41'
			 ]
others_color = '#333333'
slug_color_dict = {'DEFAULT':'#000000', 'LFDM':'#1D60B9', 'MMGE':'#E9567B', 'MYR':'#F08326'}
################################### methods that DO NOT touch DB ##################################
'''
1. 간단한 유저 인증 절차 정도만 수행
2. html을 띄워주거나(render) url로 redirect(HttpResponseRedirect) 
해주는 메서드들

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
    if (not request.user.is_authenticated or
        request.user.get_username() not in admins[1:]):
        return HttpResponseRedirect('/permission/')

    username = request.user.username
    return render_to_response('IndividualTimeSet.html', {'username': username, })

def Borrow(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    username = request.user.username
    return render_to_response('Borrow.html', {'username': username, })

##################################### methods that DO touch DB ####################################
'''
database에 접근하여 데이터를 등록, 변경, 삭제하는 메서드들

setTime      : 뜨락 월별 시간표 등록에 사용되는 알고리즘; 잘못 등록해서 다시 등록해야 할 때도 작동한다 (덮어쓰기 가능)
submit       : 뜨락 월별 시간표 등록. 시간별 동아리를 request.POST 형식으로 받아온다.
cluSubmit    : 동아리별 시간표 등록; 동아리별 admin 계정만 가능.
borrowSubmit : 타 동아리에 뜨락 시간을 빌려줄 때 사용
awakeSubmit  : 철야 등록. 이미 철야가 등록되있을 경우 차단함.
delete       : submit으로 정해진 시간 외에 각 동아리 admin 계정으로 등록한 일정을 삭제함 (club, borrow, awake 모두 포함)

TODO 
1. borrowSubmit : 자기 동아리 시간에만 빌려줄 수 있게 => 여러 동아리 시간에 걸치면?
2. ERROR Page 통일
    - 현재: permission       => 권한 없음
           * clubTimeError  => 일정의 끝시간이 시작시간보다 빠름
           * BorrowError    => 일정의 끝시간이 시작시간보다 빠름
           StayAwake        => 지정한 날짜에 이미 등록된 철야가 있음
'''
def setTime(weekList, weekday, curYear, curMonth, lastDay):
    j=1
    for aList in weekList:
        i=0
        isMorning = weekList.index(aList) == 0
        for day in aList:
            if isMorning:
                tit = '오전 공용시간\n드럼/합주 우선:\n' + slug_user_dict[day]
                c = club_colors[0]
            else:    
                tit = slug_user_dict[day]
            
            date = getFLDay(i, weekday, lastDay)
                
            for slug in slugs:
                # 자기 동아리 시간은 동아리별 시간표에서 비워둔다
                # 동아리 내 시간분배를 잘 볼 수 있게 하기 위함
                # 단, 아침은 예외
                if not isMorning and day == slug:
                    continue
                    
                if slug == 'DEFAULT' and not isMorning:
                    c = slug_color_dict[day]
                elif not isMorning:
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

@csrf_exempt
def submit(request):
    morList = list([request.POST.get('mor['+str(i)+']') for i in range(0,7)]) 
    aftList = list([request.POST.get('aft['+str(i)+']') for i in range(0,7)])
    eveList = list([request.POST.get('eve['+str(i)+']') for i in range(0,7)])
    
    weekList = [morList, aftList, eveList]
    month = request.POST.get('month')
    curYear = datetime.date.today().year
    curMonth = datetime.date.today().month
    # 사용자가 다음달 설정을 선택함
    if month != 'cur':
        curMonth = curMonth + 1
        if curMonth==13:
            curMonth = 1
            curYear += 1
    
    weekday = {'first':datetime.date(curYear, curMonth, 1).weekday(), 
               'last':datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()}
    firstWeekDay = datetime.date(curYear, curMonth, 1).weekday()
    firstDay = 1
    lastWeekDay = datetime.date(curYear, curMonth, calendar.monthrange(curYear, curMonth)[1]).weekday()
    lastDay = calendar.monthrange(curYear, curMonth)[1]

    setTime(weekList, weekday, curYear, curMonth, lastDay)

    url = '/timetable'
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
            
        Event(calendar=Calendar.objects.get(slug=slug),
              title=team,
              start=start,
              end=end,
              color_event = color,
              creator=UserModel.objects.get(username=club),
              ).save()
        
        url = '/clubTimetable'

    return HttpResponseRedirect(url)

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
def awakeSubmit(request):
    datestr = request.POST['date']
    club = request.POST['club']
    # 철야를 신청한 동아리의 calendar slug 값
    owner_slug = admin_slug_dict[club]
    color = slug_color_dict[owner_slug]

    start = (datetime.datetime.strptime(datestr, '%b %d, %Y') 
             + datetime.timedelta(days=1))
    end = start + datetime.timedelta(hours=6)
    
    # DEFAULT slug만 따로 try-except하는 이유:
    # 이미 철야가 등록된 동아리가 있는지 check하기 위함
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
            c = '#333333'
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

################################ methods that supports other methods ##############################
'''
반복 사용되는 코드를 모듈화한 메서드들

getFLDay       : submit - setTime 에서 사용
filterAccount  : delete 에서 사용
'''
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

def filterAccount(eventSet, slug):
	for account in admins:
			if slug_admin_dict[slug] == account:
			    continue
			else:
				eventSet = eventSet.exclude(creator=UserModel.objects.get(username=account))
	return eventSet
