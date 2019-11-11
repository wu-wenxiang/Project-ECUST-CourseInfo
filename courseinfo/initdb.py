#!/usr/bin/env python

import os
import django
import datetime
import xlrd

BASE_DIR = os.path.dirname(__file__)


def readWorkbook(workbookPath, x=0, index=0):
    ''' 电子表格
        workbookPath: os.path.join(BASE_DIR, 'excel', 'classroom.xls')
        x: 从x行开始 0,1,2...
        index: 工作表序号
    '''

    workbook = xlrd.open_workbook(filename=workbookPath)
    sheet = workbook.sheet_by_index(index)

    myList = []
    for row_num in range(x, sheet.nrows):
        row = sheet.row(row_num)  # row -- [empty:'', empty:'', text:'HZ-616S', number:10000.0]
        v = [r.value.strip() for r in row]
        myList.append(v)

    return myList


def syncdb(classrooms, schedules):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    if not User.objects.filter(username='admin'):
        user = User.objects.create_superuser('admin', 'admin@test.com', '56e1E@ab1234')
        user.save()

    from classroom.models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course

    # Import classroom
    items = set(i[4] for i in classrooms)
    [i.delete() for i in Campus.objects.all() if i.name not in items]
    items = items - set(Campus.objects.all().values_list('name', flat=True))
    items = [Campus(name=i) for i in items]
    Campus.objects.bulk_create(items, batch_size=20)

    items = set(i[3] for i in classrooms)
    [i.delete() for i in ClassroomType.objects.all() if i.name not in items]
    items = items - set(ClassroomType.objects.all().values_list('name', flat=True))
    items = [ClassroomType(name=i) for i in items]
    ClassroomType.objects.bulk_create(items, batch_size=20)

    items = set((i[4], i[2]) for i in classrooms)
    [i.delete() for i in Building.objects.all() if (i.campus.name, i.name) not in items]
    items = items - set(Building.objects.all().values_list('campus__name', 'name'))
    items = [Building(campus=Campus.objects.get(name=k), name=v) for (k,v) in items]
    Building.objects.bulk_create(items, batch_size=20)

    items = {i[0]:i for i in classrooms}
    [i.delete() for i in Classroom.objects.all() if i.id not in items]
    items = {i:items[i] for i in set(items)-set(Classroom.objects.all().values_list('id', flat=True))}
    items = [(v, Campus.objects.get(name=v[4])) for (k,v) in items.items()]
    items = [(i[0], Building.objects.get(campus=i[1], name=i[0][2])) for i in items]
    items = [(i[0], i[1], ClassroomType.objects.get(name=i[0][3])) for i in items]
    items = [Classroom(id=i[0][0], name=i[0][1], building=i[1], classroomType=i[2]) for i in items]
    Classroom.objects.bulk_create(items, batch_size=20)

    # Import schedule
    items = set((i[3], i[4]) for i in schedules)
    [i.delete() for i in Teacher.objects.all() if (i.id, i.name) not in items]
    items = items - set(Teacher.objects.all().values_list('id', 'name'))
    items = [Teacher(id=i[0], name=i[1]) for i in items]
    Teacher.objects.bulk_create(items, batch_size=20)

    items = set(i[1] for i in schedules)
    items = items - set(Term.objects.all().values_list('name', flat=True))
    today = datetime.date.today()
    items = [Term(name=i, firstMonday=today, start=today, end=today) for i in items]
    Term.objects.bulk_create(items, batch_size=20)


    [i.delete() for i in Course.objects.all()]
    items = [(
        i, Term.objects.get(name=i[1]), Teacher.objects.get(id=i[3]),
        Classroom.objects.get(id=i[8])) for i in schedules]
    items = [Course(
        courseid=i[0][0], term=i[1], name=i[0][2], teacher=i[2], CLASS_TIME=i[0][5],
        START_TIME=i[0][6], classroom=i[3], XQ=i[0][9], KS=i[0][10] or 0,
        JS=i[0][11] or 0, ZC1=i[0][12] or 0, ZC2=i[0][13] or 0,
        SJBZ=i[0][14] or 0, showtext=i[0][15] or 0) for i in items]
    Course.objects.bulk_create(items, batch_size=20)


if __name__ == "__main__":
    classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    classrooms = readWorkbook(classroomExcel)
    scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    schedules = readWorkbook(scheduleExcel, x=1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from classroom.models import Term

    [i.delete() for i in Term.objects.all()]
    terms = [
        ('2018-2019-1', datetime.date(2018, 9, 1), datetime.date(2018, 9, 1), datetime.date(2019, 1, 15)),
        ('2018-2019-2', datetime.date(2019, 2, 10), datetime.date(2019, 2, 10), datetime.date(2019, 6, 30)),
        ('2019-2020-1', datetime.date(2019, 9, 2), datetime.date(2019, 9, 2), datetime.date(2020, 1, 15)),
        ('2019-2020-2', datetime.date(2020, 2, 10), datetime.date(2020, 2, 10), datetime.date(2020, 6, 30)),
        ('2020-2021-1', datetime.date(2020, 9, 1), datetime.date(2020, 9, 1), datetime.date(2021, 1, 15)),
        ('2020-2021-2', datetime.date(2021, 2, 10), datetime.date(2021, 2, 10), datetime.date(2021, 6, 30))
    ]
    items = [Term(name=i[0], firstMonday=i[1], start=i[2], end=i[3]) for i in terms]
    Term.objects.bulk_create(items, batch_size=20)

    syncdb(classrooms, schedules)
