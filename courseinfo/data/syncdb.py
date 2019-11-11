#!/usr/bin/env python

from initdb import readWorkbook, syncdb
import cx_Oracle


def getData(sql):
    db = cx_Oracle.connect("jw_user", "Hdlgdx18", "172.20.8.37:1521/orcl", encoding="UTF-8")
    cur = db.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    ret = [[j or '' for j in i] for i in result]
    cur.close
    db.close()
    return ret


if __name__ == "__main__":
    import os
    BASE_DIR = os.path.dirname(__file__)

    classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    classrooms = readWorkbook(classroomExcel)
    scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    schedules = readWorkbook(scheduleExcel, x=1)
    # classrooms = getData('select * from VIEW_DJZX_CLASSROOM')
    # # print(type(classrooms[0]), classrooms[0:10])
    # schedules = getData("select * from VIEW_DJZX_SCHEDULE where TERMNAME='2019-2020-1'")
    # # print(type(schedules[0]), schedules[0:10])
    syncdb(classrooms, schedules)
