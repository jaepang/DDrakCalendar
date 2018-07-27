DDrak Calender - 화요뜨락 시간표
===============================

# Overview
본 웹사이트는 성균관대학교 자연과학캠퍼스 학생회관에 위치한 합주 겸 공연공간 화요뜨락(이하 '뜨락')의 효과적인 시간 배분과 관리를 목적으로 합니다.
###### 로그인 화면
![Alt text](/githubimages/login.png)

###### 뜨락 전체 시간표 화면
![Alt text](/githubimages/timetable_default.png)

###### 동아리별 시간표 화면
![Alt text](/githubimages/timetable_club.png)


# 사용 매뉴얼 (for 악의꽃, 막무간애, 모여락)
사이트 url
-------------------
<http://ddrakcalendar.pythonanywhere.com>

계정들 (accounts)
-------------------
*로그인화면에 "동아리 이름"란에 작성하는 ID입니다(GUEST 제외).*
1. admin : 전체 관리자
	* 막악모 시간 배분 설정 가능
	![Alt text](/githubimages/setTime.png)
	* 사이트 admin 권한을 부여함 (django admin page에 접속 가능)
    *for developers*

2.  악의꽃admin, 막무간애admin, 모여락admin : 동아리 뜨락지기 계정
	* 동아리 내의 팀 별 시간 설정

	    > 동아리 시간표에만 적용됩니다.

	![Alt text](/githubimages/set_club_time.png)
	* 철야 설정
	* 타 동아리에 시간 대여해주기
	    > 시간 설정화면은 팀 별 시간설정과 같지만, 대여 설정은 전체 시간표 및 타 동아리 시간표에도 적용됩니다.

	* 설정한 시간(팀 별 시간, 철야, 대여)을 클릭하면 삭제 가능
	![Alt text](/githubimages/delete_event.PNG)
	__대여의 경우 계정이 속한 동아리가 대여해준 시간만 삭제 가능합니다.__

3. 악의꽃, 막무간애, 모여락 : 동아리 부원 계정
	* 각 동아리 시간표 열람 가능
	* 각 일정을 누르면 일정 제목, 시작시간, 끝시간 열람 가능
	![Alt text](/githubimages/see_event.PNG)
4. GUEST : 동아리 외 인원
	* 전체 시간표 열람 가능

주의사항
-------------------
1. 동아리별 시간표에서 __빈 공간이 동아리 시간입니다!!!__
2. admin 계정은 동아리별 시간표를 열람할 수 없습니다.
3. 동아리부원, 뜨락지기 계정은 전체 시간표 및 본인 동아리 시간표만 열람할 수 있습니다.
즉, 모든 시간표를 열람할 수 있는 계정은 없습니다.
4. 본 사이트는 Windows 10, Google Chrome에 최적화되어 있습니다.
