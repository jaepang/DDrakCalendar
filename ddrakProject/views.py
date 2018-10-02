from django.shortcuts import render_to_response, HttpResponse
from schedule.models import Calendar, Event, Rule
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime, calendar, random

UserModel = get_user_model()

@csrf_exempt
def delete(request):
    title = request.POST.get('title')
    startStr = request.POST.get('start')
    endStr = request.POST.get('end')
    account = request.POST.get('username')
    start = datetime.datetime.strptime(startStr, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(endStr, '%Y-%m-%d %H:%M:%S')
    if account == '악의꽃admin':
        slug = 'LFDM'
    elif account == '막무간애admin':
        slug = 'MMGE'
    elif account == '모여락admin':
        slug = 'MYR'
    try:
        delete = Event.objects.get(title=title,
                                   start=start,
                                   end=end,
                                  )
        if delete.creator.username != account:
            return HttpResponseRedirect('/permission/')
        else:
            delete.delete()
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/permission/')
    except Event.MultipleObjectsReturned:
        eventSet = Event.objects.filter(title=title,
                                        start=start,
                                        end=end,
                                        )
        if slug=='LFDM':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='막무간애admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='모여락admin'))
        elif slug=='MMGE':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='악의꽃admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='모여락admin'))
        elif slug=='MYR':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='막무간애admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='악의꽃admin'))
        eventSet.delete()
    if title == '철야':
        eventSet = Event.objects.filter(title=account,
                                        start=start,
                                        end=end,
                                        )
        if slug=='LFDM':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='막무간애admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='모여락admin'))
        elif slug=='MMGE':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='악의꽃admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='모여락admin'))
        elif slug=='MYR':
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='막무간애admin'))
            eventSet = eventSet.exclude(creator=UserModel.objects.get(username='악의꽃admin'))
        eventSet.delete()

    if account == '악의꽃admin':
        return HttpResponseRedirect('/LFDMtimetable/')
    elif account == '막무간애admin':
        return HttpResponseRedirect('/MMGEtimetable/')
    elif account == '모여락admin':
        return HttpResponseRedirect('/MYRtimetable/')



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
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


def Initialize(request):
    return HttpResponseRedirect('/accounts/login/')


def LFDM(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '악의꽃' and request.user.get_username() != '악의꽃admin' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    user = request.user

    return render_to_response('LFDMtimetable.html', {'user': user, })


def MMGE(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '막무간애' and request.user.get_username() != '막무간애admin' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    user = request.user

    return render_to_response('MMGEtimetable.html', {'user': user, })


def MYR(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '모여락' and request.user.get_username() != '모여락admin' and request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    user = request.user

    return render_to_response('MYRtimetable.html', {'user': user, })


def SetTime(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != 'admin':
        return HttpResponseRedirect('/permission/')

    return render_to_response('SetTime.html')


def StayAwake(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/permission/')

    elif request.user.get_username() != '악의꽃admin' and request.user.get_username() != '막무간애admin' and request.user.get_username() != '모여락admin':
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


@csrf_exempt
def borrowSubmit(request):
    color_set = ['#e53935', '#d81b60', '#8e24aa',
                 '#3949ab', '#1e88e5', '#039be5',
                 '#00acc1', '#00897b', '#43a047',
                 '#7cb342', '#827717', '#33691e',
                 '#ff6f00', '#e64a19', '#6d4c41']
    date = request.POST.getlist('date')
    time = request.POST.getlist('time')
    team = request.POST.get('teamname')
    club = request.POST.get('club')
    # Jul 13, 2018 12:30 PM
    start = datetime.datetime.strptime(
        date[0]+' '+time[0], '%b %d, %Y %I:%M %p')
    end = datetime.datetime.strptime(date[1]+' '+time[1], '%b %d, %Y %I:%M %p')
    color = random.choice(color_set)
    if end < start:
        url = '/BorrowError'
        return HttpResponseRedirect(url)

    url = '/timetable'
    if club == '악의꽃admin':
        url = '/LFDMtimetable'
    elif club == '막무간애admin':
        url = '/MMGEtimetable'
    elif club == '모여락admin':
        url = '/MYRtimetable'
    event1 = Event(calendar=Calendar.objects.get(slug='MYR'),
                  title=team,
                  start=start,
                  end=end,
                  color_event=color,
                  creator=UserModel.objects.get(username=club),
                  )
    event2 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                  title=team,
                  start=start,
                  end=end,
                  color_event=color,
                  creator=UserModel.objects.get(username=club),
                  )
    event3 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                  title=team,
                  start=start,
                  end=end,
                  color_event=color,
                  creator=UserModel.objects.get(username=club),
                  )
    event4 = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                  title=team,
                  start=start,
                  end=end,
                  color_event=color,
                  creator=UserModel.objects.get(username=club),
                  )
    event1.save()
    event2.save()
    event3.save()
    event4.save()

    return HttpResponseRedirect(url)


@csrf_exempt
def clubSubmit(request):
    color_set = ['#e53935', '#d81b60', '#8e24aa',
                 '#3949ab', '#1e88e5', '#039be5',
                 '#00acc1', '#00897b', '#43a047',
                 '#7cb342', '#827717', '#33691e',
                 '#ff6f00', '#e64a19', '#6d4c41']
    date = request.POST.getlist('date')
    time = request.POST.getlist('time')
    team = request.POST.get('teamname')
    club = request.POST.get('club')
    # Jul 13, 2018 12:30 PM
    start = datetime.datetime.strptime(date[0]+' '+time[0], '%b %d, %Y %I:%M %p')
    end = datetime.datetime.strptime(date[1]+' '+time[1], '%b %d, %Y %I:%M %p')
    color = random.choice(color_set)
    if end < start:
        url = '/ClubTimeError'
        return HttpResponseRedirect(url)

    url = '/timetable'
    if club == '악의꽃' or club == '악의꽃admin':
        event = Event(calendar=Calendar.objects.get(slug='LFDM'),
                      title=team,
                      start=start,
                      end=end,
                      color_event = color,
                      creator=UserModel.objects.get(username=club),
                     )
        event.save()
        url = '/LFDMtimetable'
    elif club == '막무간애' or club == '막무간애admin':
        event = Event(calendar=Calendar.objects.get(slug='MMGE'),
                      title=team,
                      start=start,
                      end=end,
                      color_event = color,
                      creator=UserModel.objects.get(username=club),
                     )
        event.save()
        url = '/MMGEtimetable'
    elif club == '모여락' or club == '모여락admin':
        event = Event(calendar=Calendar.objects.get(slug='MYR'),
                      title=team,
                      start=start,
                      end=end,
                      color_event = color,
                      creator=UserModel.objects.get(username=club),
                     )
        event.save()
        url = '/MYRtimetable'

    return HttpResponseRedirect(url)


@csrf_exempt
def awakeSubmit(request):
    datestr = request.POST['date']
    club = request.POST['club']
    if club == '악의꽃' or club == '악의꽃admin':
        flag = 1
        color = '#1D60B9'
    elif club == '막무간애' or club == '막무간애admin':
        flag = 2
        color = '#E9567B'
    elif club == '모여락' or club == '모여락admin':
        flag = 3
        color = '#F08326'
    others_color = '#777777'

    start = datetime.datetime.strptime(datestr, '%b %d, %Y') + datetime.timedelta(days=1)
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
                      title=club,
                      start=start,
                      end=end,
                      color_event = color,
                      creator=UserModel.objects.get(username=club),
                     )
        event.save()

    # 악꽃 시간표를 막, 모에 전달
    if flag == 1:
        event1 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                       title=club,
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                      )
        event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                       title=club,
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                       )
        event3= Event(calendar=Calendar.objects.get(slug='LFDM'),
                       title='철야',
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                       )
        event1.save()
        event2.save()
        event3.save()

    # 막간 시간표를 악, 모에 전달
    elif flag == 2:
        event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                       title=club,
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                      )
        event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                       title=club,
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                       )
        event3 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                       title='철야',
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                       )
        event1.save()
        event2.save()
        event3.save()

    # 모여락 시간표를 악, 막에 전달
    elif flag == 3:
        event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                        title=club,
                        start=start,
                        end=end,
                        color_event=others_color,
                        creator=UserModel.objects.get(username=club),
                        )
        event2 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                        title=club,
                        start=start,
                        end=end,
                       color_event=others_color,
                        creator=UserModel.objects.get(username=club),
                        )
        event3 = Event(calendar=Calendar.objects.get(slug='MYR'),
                       title='철야',
                       start=start,
                       end=end,
                       color_event=others_color,
                       creator=UserModel.objects.get(username=club),
                       )
        event1.save()
        event2.save()
        event3.save()

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
    weekList = [aftList, eveList]
    month = request.POST.get('month')
    others_color = '#777777'
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

            # try-except to update
            try:
                event = Event.objects.get(calendar=Calendar.objects.get(slug='DEFAULT'),
                                          start=datetime.datetime(
                                              curYear, curMonth, fday, j*6, 0),
                                          end=datetime.datetime(
                                              curYear, curMonth, fday, j*6+5, 59),
                                         )
                Event.objects.filter(calendar=Calendar.objects.get(slug='DEFAULT'),
                                     start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                     end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                     ).update(title=tit, color_event=color, creator=UserModel.objects.get(username='admin'),)
            except ObjectDoesNotExist:
                event = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                              title=tit,
                              start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                              end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                              rule=Rule.objects.get(id=3), # Weekly;
                              end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                              color_event = color,
                              creator=UserModel.objects.get(username='admin'),
                              )
                event.save()

            # 악꽃 시간표를 막, 모에 전달
            if flag == 1:
                try:
                    event1 = Event.objects.get(calendar=Calendar.objects.get(slug='MMGE'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                              )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='MMGE'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event1 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin'),
                                  )
                    event1.save()
                try:
                    event2 = Event.objects.get(calendar=Calendar.objects.get(slug='MYR'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                              )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='MYR'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin'),
                                  )
                    event2.save()

                # 이미 있던 다른 동아리 시간 삭제
                try:
                    Event.objects.get(calendar=Calendar.objects.get(slug='LFDM'),
                                      start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                      end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                      ).delete()
                except ObjectDoesNotExist:
                    pass

            # 막간 시간표를 악, 모에 전달
            elif flag == 2:
                try:
                    event1 = Event.objects.get(calendar=Calendar.objects.get(slug='LFDM'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                              )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='LFDM'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin'),
                                   )
                    event1.save()
                try:
                    event2 = Event.objects.get(calendar=Calendar.objects.get(slug='MYR'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                               )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='MYR'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event2 = Event(calendar=Calendar.objects.get(slug='MYR'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin')
                                   )
                    event2.save()

                # 이미 있던 다른 동아리 시간 삭제
                try:
                    Event.objects.get(calendar=Calendar.objects.get(slug='MMGE'),
                                      start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                      end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                      ).delete()
                except ObjectDoesNotExist:
                    pass

            # 모여락 시간표를 악, 막에 전달
            elif flag == 3:
                try:
                    event1 = Event.objects.get(calendar=Calendar.objects.get(slug='LFDM'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                               )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='LFDM'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event1 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin')
                                   )
                    event1.save()
                try:
                    event2 = Event.objects.get(calendar=Calendar.objects.get(slug='MMGE'),
                                               start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                               end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                               )
                    Event.objects.filter(calendar=Calendar.objects.get(slug='MMGE'),
                                         start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                         end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                         ).update(title=tit, color_event=others_color, creator=UserModel.objects.get(username='admin'),)
                except ObjectDoesNotExist:
                    event2 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                                   title=tit,
                                   start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                   end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                   rule=Rule.objects.get(id=3),  # Weekly;
                                   end_recurring_period=datetime.datetime(curYear, curMonth, lday, j*6+5, 59),
                                   color_event=others_color,
                                   creator=UserModel.objects.get(username='admin')
                                   )
                    event2.save()

                # 이미 있던 다른 동아리 시간 삭제
                try:
                    Event.objects.get(calendar=Calendar.objects.get(slug='MYR'),
                                      start=datetime.datetime(curYear, curMonth, fday, j*6, 0),
                                      end=datetime.datetime(curYear, curMonth, fday, j*6+5, 59),
                                      ).delete()
                except ObjectDoesNotExist:
                    pass

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

            try:
                event1 = Event.objects.get(calendar=Calendar.objects.get(slug='DEFAULT'),
                                           start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                           end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                           )
                Event.objects.filter(calendar=Calendar.objects.get(slug='DEFAULT'),
                                     start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                     end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                     ).update(title=tit, creator=UserModel.objects.get(username='admin'))
            except ObjectDoesNotExist:
                event1 = Event(calendar=Calendar.objects.get(slug='DEFAULT'),
                               title=tit,
                               start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                               end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                               rule=Rule.objects.get(id=3),  # Weekly;
                               end_recurring_period=datetime.datetime(curYear, curMonth, lday, 11, 59),
                               creator=UserModel.objects.get(username='admin')
                            )
                event1.save()

            try:
                event2 = Event.objects.get(calendar=Calendar.objects.get(slug='LFDM'),
                                           start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                           end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                           )
                Event.objects.filter(calendar=Calendar.objects.get(slug='LFDM'),
                                     start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                     end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                     ).update(title=tit, creator=UserModel.objects.get(username='admin'))
            except ObjectDoesNotExist:
                event2 = Event(calendar=Calendar.objects.get(slug='LFDM'),
                               title=tit,
                               start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                               end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                               rule=Rule.objects.get(id=3),  # Weekly;
                               end_recurring_period=datetime.datetime(curYear, curMonth, lday, 11, 59),
                               creator=UserModel.objects.get(username='admin')
                               )
                event2.save()
            try:
                event3 = Event.objects.get(calendar=Calendar.objects.get(slug='MMGE'),
                                           start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                           end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                           )
                Event.objects.filter(calendar=Calendar.objects.get(slug='MMGE'),
                                     start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                     end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                     ).update(title=tit, creator=UserModel.objects.get(username='admin'))
            except ObjectDoesNotExist:
                event3 = Event(calendar=Calendar.objects.get(slug='MMGE'),
                               title=tit,
                               start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                               end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                               rule=Rule.objects.get(id=3),  # Weekly;
                               end_recurring_period=datetime.datetime(curYear, curMonth, lday, 11, 59),
                               creator=UserModel.objects.get(username='admin'),
                               )
                event3.save()
            try:
                event4 = Event.objects.get(calendar=Calendar.objects.get(slug='MYR'),
                                           start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                           end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                           )
                Event.objects.filter(calendar=Calendar.objects.get(slug='MYR'),
                                     start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                                     end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                                     ).update(title=tit, creator=UserModel.objects.get(username='admin'))
            except ObjectDoesNotExist:
                event4 = Event(calendar=Calendar.objects.get(slug='MYR'),
                               title=tit,
                               start=datetime.datetime(curYear, curMonth, fday, 6, 0),
                               end=datetime.datetime(curYear, curMonth, fday, 11, 59),
                               rule=Rule.objects.get(id=3),  # Weekly;
                               end_recurring_period=datetime.datetime(curYear, curMonth, lday, 11, 59),
                               creator=UserModel.objects.get(username='admin')
                               )
                event4.save()

            i += 1

    url = '/timetable'
    return HttpResponseRedirect(url)
