from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course
from myAPI.pageAPI import djangoPage,PAGE_NUM,toInt
from myAPI.dateAPI import get_year_weekday, get_weekday, get_date
from myAPI.listAPI import pinyin, get_english


def get_year_whichweek_week(date_str):
    """ 例如：date_str='2019-09-02' 2019秋季开学第一学期，初始化值('2020-1')
        返回数据含意               ('2019秋季开学第一学期', 相对开学第几周(开学是第1周), 星期几, 1或2)
        date_str = '2019-09-02'    返回 '2020-1' 1 1 1
        date_str = '2019-09-25'    返回 '2020-1' 4 3 2

        数据格式含意：
        1、2019-2020-1：2019秋季开学第一学期；
        2、开学时间（学校规定）：2019-09-02；
        3、数据库字段SJBZ：只有0、1、2三个数字，0代表每周都有课，1代表单数周有课，2代表双数周有课
    """
    if '2019-09' in date_str:
        date_str0 = '2019-09-02' #2019-09-02开学
    else: return '',0,0,0
    s0 = get_year_weekday(date_str0)
    s1 = get_year_weekday(date_str)
    if s0[0] != s1[0]: return '',0,0,0
    w = s1[1] - s0[1] + 1 #相对开学第几周
    sjbz=2 if w%2 == 0 else 1 #sjbz:1代表单数周有课，2代表双数周有课
    return '%s-1'%(s0[0]+1), w, s1[2], sjbz

def get_update_downdate(cleanData):
    """ 今天 上一天 下一天
        返回 类似这样：2019-09-28,0
    """
    todaydate = cleanData.get('todaydate','')
    date = cleanData.get('date','')
    update = cleanData.get('update','')
    downdate = cleanData.get('downdate','')
    count = cleanData.get('count','')
    count = int(count) if count else 0
    if todaydate:  count = 0 #今天
    if update:  count -=  1 #上一天
    if downdate: count += 1 #下一天
    data_str = date if date else get_date(count)
    return data_str,count


def test(request):
    date_str = '2019-09-02'
    return HttpResponse(get_year_whichweek_week(date_str))

def _filter_model(models, date_str):
    """ 按时间过滤
        models： 数据库记录
        date_str： 时间字符串 '2019-09-29'
        返回过滤后的数据库记录
    """
    model = ''
    TERMNAME,whichweek,week, sjbz = get_year_whichweek_week(date_str)
    if TERMNAME:
        model = models.filter(TERMNAME__icontains = TERMNAME,\
                ZC1__lte = whichweek, ZC2__gte = whichweek,\
                XQ__icontains = str(week), SJBZ = sjbz).order_by("-id")|\
                models.filter(TERMNAME__icontains = TERMNAME, \
                ZC1__lte = whichweek,ZC2__gte = whichweek,\
                XQ__icontains = str(week), SJBZ = 0).order_by("-id")
    return  model



SEARCH_LIST = ['按教室分布查','按课程名称查','按教师名称查'] #查询列表

#课程查询、自习室查询 查询
def index(request):
    query_list = ['课程查询','自习室查询'] #查询列表

    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken') #删除字典中的键'csrfmiddlewaretoken'和值
        queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])
        if cleanData['query'] == query_list[0]:
            search_list = SEARCH_LIST
            return render(request, 'classroom/class_list.html', context=locals())

        if cleanData['query'] == query_list[1]:
            return HttpResponseRedirect('/self/building/list/%s' %queryString)
    return render(request, 'classroom/query_list.html', context=locals())


def choice(request, page):
    search_list = SEARCH_LIST
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



# 按教室分布查  校区 -- 教学楼列表
def building_list(request):
    cleanData = request.GET.dict()
    campus_list = Campus.objects.values_list('name', flat=True)
    campus_list = pinyin(campus_list)
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken')
        if cleanData.get('campus',''):
            campus = cleanData['campus']
            buildings = list(set(Building.objects.filter(\
                    campus=campus).values_list('name', flat=True))) #教学楼列表
            buildings = pinyin(buildings)
            return render(request, 'classroom/building_list.html', context=locals())
    return render(request, 'classroom/campus_list.html', context=locals())


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

#自习室查询
#校区 -- 教学楼列表
def self_building_list(request):
    cleanData = request.GET.dict()
    campus_list = Campus.objects.values_list('name', flat=True) #校区列表
    campus_list = pinyin(campus_list)
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken')

        campus = cleanData.get('campus','') #校区
        buildings = Building.objects.filter(campus=campus).values_list('name', flat=True) #教学楼列表
        if campus == '奉贤校区':
            buildings = get_english(buildings)
        buildings = pinyin(buildings)
        return render(request, 'classroom/self_building_list.html', context=locals())
    return render(request, 'classroom/self_campus_list.html', context=locals())


# 自习教室查询
def self_study_list(request):
    """1、自习教室是 教室类型为多媒体教室，并且课程为空的课节

    """
    cleanData = request.GET.dict()
    if request.method == 'POST':
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken')
    data_str,count = get_update_downdate(cleanData) # 2019-09-28,0

    query,campus,building,room = cleanData.get('query',''),cleanData.get('campus',''),\
            cleanData.get('building',''),cleanData.get('room','') #查询 校区 教学楼名称

    weekday = get_weekday(data_str)

    #获得 教室类型为多媒体教室的id
    room_ids = list(Classroom.objects.filter(type='多媒体教室', campus=campus, building=building).values_list('ROOM_ID', flat=True))

    models = Schedule.objects.filter(CLASSROOM_ID='xxxx') #空记录
    for room_id in room_ids:
        models = models | Schedule.objects.filter(CLASSROOM_ID=room_id)

    data_list = []
    datas = _filter_model(models, data_str) #data_str时间过滤
    if datas:
        #获得教室名列表
        classroom_names = list(set(datas.filter().values_list('CLASSROOM_NAME', flat=True)))
        for classroom_name in classroom_names:
            model_list = datas.filter(CLASSROOM_NAME=classroom_name)
            mlist = ['','','','','','','','','','','','']

            for model in model_list:
                ks = model.KS
                js = model.JS
                for n in range(ks-1,js):
                    mlist[n] = (n+1)

            if any(mlist):
                mlist.insert(0, classroom_name) #插入教室名
                mlist.insert(1,Classroom.objects.filter(ROOM_NAME=classroom_name).first().TYPE)#插入教室类型
                data_list.append(mlist)
    return render(request, 'classroom/self_study_list.html', context=locals())
