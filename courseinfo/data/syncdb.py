#!/usr/bin/env python

import os
import django
import datetime
import cx_Oracle

BASE_DIR = os.path.dirname(__file__)


def getData(dbName):
    db = cx_Oracle.connect("jw_user", "Hdlgdx18", "172.20.8.37:1521/orcl", encoding="UTF-8")
    cur = db.cursor()
    sql = "select * from %s" % dbName
    cur.execute(sql)
    result = cur.fetchall()
    ret = [list(i) for i in result]
    cur.close
    db.close()
    return ret


if __name__ == "__main__":
    # classrooms = getData('VIEW_DJZX_CLASSROOM')
    # # print(type(classrooms[0]), classrooms[0:10])
    # schedules = getData('VIEW_DJZX_SCHEDULE')
    # # print(type(schedules[0]), schedules[0:10])

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from classroom.models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course

    # # Import classroom
    # classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    # workbookList = readWorkbook(classroomExcel)

    # items = [Campus(name=j) for j in set(i[4] for i in workbookList)]
    # Campus.objects.bulk_create(items, batch_size=20)

    # items = [ClassroomType(name=j) for j in set(i[3] for i in workbookList)]
    # ClassroomType.objects.bulk_create(items, batch_size=20)

    # items = set([(i[4], i[2]) for i in workbookList])
    # items = [Building(campus=Campus.objects.get(name=k), name=v) for (k,v) in items]
    # Building.objects.bulk_create(items, batch_size=20)

    # items = {i[0]:i for i in workbookList}
    # items = [(v, Campus.objects.get(name=v[4])) for (k,v) in items.items()]
    # items = [(i[0], Building.objects.get(campus=i[1], name=i[0][2])) for i in items]
    # items = [(i[0], i[1], ClassroomType.objects.get(name=i[0][3])) for i in items]
    # items = [Classroom(id=i[0][0], name=i[0][1], building=i[1], classroomType=i[2]) for i in items]
    # Classroom.objects.bulk_create(items, batch_size=20)

    # # Import schedule
    # scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    # workbookList = readWorkbook(scheduleExcel, x=1)

    # items = [Teacher(id=j[0], name=j[1]) for j in set((i[3],i[4]) for i in workbookList)]
    # Teacher.objects.bulk_create(items, batch_size=20)

    # items = [Term(name=j, firstMonday=datetime.datetime.now()) for j in set(i[1] for i in workbookList)]
    # Term.objects.bulk_create(items, batch_size=20)

    # items = {i[0]:i for i in workbookList}
    # items = [(
    #     v, Term.objects.get(name=v[1]), Teacher.objects.get(id=v[3]),
    #     Classroom.objects.get(id=v[8])) for (k,v) in items.items()]
    # items = [Course(
    #     id=i[0][0], term=i[1], name=i[0][2], teacher=i[2], CLASS_TIME=i[0][5],
    #     START_TIME=i[0][6], classroom=i[3], XQ=i[0][9], KS=int(i[0][10]),
    #     JS=i[0][11] or 0, ZC1=i[0][12] or 0, ZC2=i[0][13] or 0,
    #     SJBZ=i[0][14] or 0, showtext=i[0][15] or 0) for i in items]
    # Course.objects.bulk_create(items, batch_size=20)