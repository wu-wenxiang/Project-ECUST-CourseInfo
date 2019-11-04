from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import datetime
from functools import reduce

from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course
from myAPI.pageAPI import djangoPage,PAGE_NUM,toInt
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

def courseInfo(request):
    return render(request, 'classroom/info-course.html', context=locals())

def campusInfo(request):
    campuses = Campus.objects.filter(show_classroom=True).values_list('name', flat=True)
    return render(request, 'classroom/info-campus.html', context=locals())

def buildingInfo(request, campus):
    buildings = Building.objects.filter(campus=campus).filter(
        campus__show_classroom=True, show_classroom=True).values_list('name', flat=True)
    return render(request, 'classroom/info-building.html', context=locals())

def classroomInfo(request, campus, building):
    cleanData = request.GET.dict()
    date = cleanData.get('date', '').strip()
    try:
        date = datetime.date.fromisoformat(date)
    except:
        date = datetime.date.today()

    classrooms = Classroom.objects.filter(
        building__campus=campus, building__campus__show_classroom=True,
        building__name=building, building__show_classroom=True,
        classroomType__show_classroom=True, show_classroom=True)
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

def choice(request, page):
    cleanData = request.GET.dict()
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken') #删除字典中的键'csrfmiddlewaretoken'和值
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])

    #按教室分布查
    if cleanData.get(search_list[0],''):
        return HttpResponseRedirect('/building/list/%s' %queryString)

    #按课程名称查
    if cleanData.get(search_list[1],''):
        return HttpResponseRedirect('/classname/list/%s' %queryString)

    #按教师姓名查
    if cleanData.get(search_list[2],''):
        return HttpResponseRedirect('/teacher/list/%s' %queryString)

#按教师姓名查
def teacher_list(request, page):
    cleanData = request.GET.dict()
    models = Course.objects.filter()
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken')

    if cleanData.get('teacher', ''):
        models = models.filter(TEACHER_NAME__icontains = cleanData['teacher'])

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])
    data_list, pageList, num_pages, page = djangoPage(models,page,PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/teacher_list.html', context=locals())


#按课程名称查
def classname_list(request, page):
    cleanData = request.GET.dict()
    models = Schedule.objects.filter()
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken')

    if cleanData.get('kcmc', ''):
        models = models.filter(KCMC__icontains = cleanData['kcmc'])

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])
    data_list, pageList, num_pages, page = djangoPage(models,page,PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/classname_list.html', context=locals())


#教学楼 -- 教室列表
def room_list(request):
    if request.method == 'POST':
        cleanData = request.POST.dict()
        rooms = list(set(Classroom.objects.filter(BUILDING =\
            cleanData.get('building','')).values_list('ROOM_NAME', flat=True))) #教室列表
        rooms = pinyin(rooms)
    return render(request, 'classroom/room_list.html', context=locals())


#教室、时间 -- 教室课程表
def kcmc_details(request):
    cleanData = request.GET.dict()
    if request.method == 'POST':
        cleanData = request.POST.dict()

    data_str,count = get_update_downdate(cleanData) # 2019-09-28,0

    query,campus,building,room = cleanData.get('query',''),cleanData.get('campus',''),\
            cleanData.get('building',''),cleanData.get('room','')

    weekday = get_weekday(data_str)
    models = Schedule.objects.filter(CLASSROOM_NAME__icontains = \
            cleanData.get('room', '')) #由教室名 获得记录   信息楼109A
    data_list =  _filter_model(models, data_str)

    mylist = []
    for n in range(0,12):
        mylist.append(['','','',''])

    for model in data_list:
        ks = model.KS
        js = model.JS
        for n in range(ks-1,js):
            mylist[n] = [model.START_TIME, model.KCMC, model.TEACHER_NAME,model.CLASSROOM_ID]

    mlist = []
    k = ['j','START_TIME','KCMC','TEACHER_NAME','CLASSROOM_ID']
    for (index,m) in enumerate(mylist):
        v = ['第%s节'%(index+1), m[0], m[1], m[2], m[3]]
        d = dict(zip(k,v))
        mlist.append(d)
    return render(request, 'classroom/kcmc_details_list.html', context=locals())

def course_list(request):
    cleanData = request.GET.dict()
    date_str = cleanData.get('date','2000-01-01')
    cid = cleanData.get('cid',1)

    weekday = get_weekday(date_str)
    models = Schedule.objects.filter(KCMC = cleanData.get('kcmc',''),\
                        TEACHER_NAME = cleanData.get('t',''))
    data_list = _filter_model(models, date_str)
    campus = Classroom.objects.filter(ROOM_ID=cid).first().CAMPUS
    building = Classroom.objects.filter(ROOM_ID=cid).first().BUILDING
    room = Classroom.objects.filter(ROOM_ID=cid).first().ROOM_NAME
    return render(request, 'classroom/course_details_list.html', context=locals())
