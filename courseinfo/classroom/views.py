from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import datetime
from functools import reduce

from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course
from myAPI.pageAPI import djangoPage, PAGE_NUM, toInt
from myAPI.dateAPI import get_year_weekday, get_weekday, get_date
from myAPI.listAPI import pinyin


def _getDateInfo(date):
    year, month = date.year, date.month
    term = '%d-%d-%d' % ((year, year+1, 1) if month > 8 else (year-1, year, 2))
    isocalendar = date.isocalendar()
    firstMonday = Term.objects.get(name=term).firstMonday
    week = (date-firstMonday).days//7 + 1
    weekday = isocalendar[2]
    return term, week, weekday

def index(request):
    return render(request, 'classroom/index.html', context=locals())

def campusInfo(request):
    baseUrl = '/classroominfo'
    campuses = Campus.objects.filter(show_classroom=True).values_list('name', flat=True)
    return render(request, 'classroom/info-campus.html', context=locals())

def buildingInfo(request, campus):
    baseUrl = '/classroominfo'
    buildings = Building.objects.filter(
        campus=campus,
        campus__show_classroom=True,
        show_classroom=True
    ).values_list('name', flat=True)
    return render(request, 'classroom/info-building.html', context=locals())

def classroomInfo(request, campus, building):
    cleanData = request.GET.dict()
    date = cleanData.get('date', '').strip()
    try:
        date = datetime.date.fromisoformat(date)
    except:
        date = datetime.date.today()

    classrooms = Classroom.objects.filter(
        building__campus=campus,
        building__campus__show_classroom=True,
        building__name=building,
        building__show_classroom=True,
        classroomType__show_classroom=True,
        show_classroom=True
    ).order_by("name")
    term, week, weekday = _getDateInfo(date)

    classroomList = []
    for i in classrooms:
        courses = Course.objects.filter(
            classroom__id=i.id,
            term=term,
            ZC1__lte = week,
            ZC2__gte = week,
            XQ=weekday,
        )
        # print(i, i.id, list(courses))
        courses = list(courses.filter(SJBZ=0)) + list(courses.filter(SJBZ=(week%2)))

        # print(i, [(j, j.KS, j.JS) for j in courses])
        idles = [j for j in range(1, 13)]
        for j in courses:
            for k in range(j.KS-1, j.JS):
                idles[k] = ''
        classroomList.append((i, idles))

    return render(request, 'classroom/info-classroom.html', context=locals())

def courseInfo(request):
    return render(request, 'classroom/info-course.html', context=locals())

def courseCampus(request):
    baseUrl = '/courseinfo/classroom'
    campuses = Campus.objects.filter(show_schedule=True).values_list('name', flat=True)
    return render(request, 'classroom/info-campus.html', context=locals())

def courseBuilding(request, campus):
    baseUrl = '/courseinfo/classroom'
    buildings = Building.objects.filter(
        campus=campus,
        campus__show_schedule=True,
        show_schedule=True
    ).values_list('name', flat=True)
    return render(request, 'classroom/info-building.html', context=locals())

def courseClassroom(request, campus, building):
    baseUrl = '/courseinfo/classroom'
    classrooms = Classroom.objects.filter(
        building__campus=campus,
        building__campus__show_schedule=True,
        building__name=building,
        building__show_schedule=True,
        classroomType__show_schedule=True,
        show_schedule=True
    ).order_by("name").values_list('name', flat=True)
    return render(request, 'classroom/info-classroom-list.html', context=locals())

def courseNameSearch(request, page):
    cleanData = request.GET.dict()
    coursename = cleanData.get('coursename', '').strip()

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for (k,v) in cleanData.items()])
    baseUrl = '/courseinfo/coursename'

    courses = Course.objects.filter()
    if coursename:
        courses = courses.filter(name__icontains = coursename)
    data_list, pageList, num_pages, page = djangoPage(courses, page, PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/search-coursename.html', context=locals())

def teacherNameSearch(request, page):
    cleanData = request.GET.dict()
    teachername = cleanData.get('teachername', '').strip()

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for (k,v) in cleanData.items()])
    baseUrl = '/courseinfo/teachername'

    courses = Course.objects.filter()
    if teachername:
        courses = courses.filter(teacher__name__icontains = teachername)
    data_list, pageList, num_pages, page = djangoPage(courses, page, PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/search-teachername.html', context=locals())
