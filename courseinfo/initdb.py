#!/usr/bin/env python

import os
import sys
import django
import random
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
    sheet = workbook.sheet_by_index(0)

    myList = []
    for row_num in range(0, sheet.nrows):
        row = sheet.row(row_num) # row -- [empty:'', empty:'', text:'HZ-616S', number:10000.0]
        v = [r.value for r in row]
        myList.append(v)

    return myList

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    from classroom.models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course

    user = User.objects.create_superuser('admin', 'admin@test.com', '56e1E@ab1234')
    user.save()

    # Import classroom
    classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    workbookList = readWorkbook(classroomExcel)

    items = [Campus(name=j) for j in set([i[4] for i in workbookList])]
    Campus.objects.bulk_create(items, batch_size=20)

    items = [ClassroomType(name=j) for j in set([i[3] for i in workbookList])]
    ClassroomType.objects.bulk_create(items, batch_size=20)

    items = set([(i[4], i[2]) for i in workbookList])
    items = [Building(campus=Campus.objects.get(name=k), name=v) for (k,v) in items]
    Building.objects.bulk_create(items, batch_size=20)

    items = {i[0]:i for i in workbookList}
    items = [(v, Campus.objects.get(name=v[4])) for (k,v) in items.items()]
    items = [(i[0], Building.objects.get(campus=i[1], name=i[0][2])) for i in items]
    items = [(i[0], i[1], ClassroomType.objects.get(name=i[0][3])) for i in items]
    items = [Classroom(id=i[0][0], name=i[0][1], building=i[1], classroomType=i[2]) for i in items]
    Classroom.objects.bulk_create(items, batch_size=20)

    # Import schedule
    scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    workbookList = readWorkbook(scheduleExcel)
    items = [Teacher(id=j[0], name=j[1]) for j in set([(i[3],i[4]) for i in workbookList])]
    Teacher.objects.bulk_create(items, batch_size=20)

    # for i in range(MATERIAL_NUM):
    #     m = Material()
    #     m.name = '材料-%s' % i
    #     m.price = random.randint(100, 200)
    #     m.save()
    
    # for i in range(COMPANY_NUM):
    #     user = User.objects.create_user('cx%s' % i, 'cx%s@test.com' % i,
    #                                     '@aB1234')
    #     user.is_staff = True
    #     user.is_superuser = False
    #     user.groups.add(customerGroup)
    #     user.save()   
    
    # cxs = User.objects.filter(groups__name='Customer')
    # ops = User.objects.filter(groups__name='Operator')

    # for i in range(COMPANY_NUM):
    #     c = Company()
    #     c.name = "公司-%s" % i
    #     if i % 3:
    #         c.taxNumber = '1234567'
    #         c.bank = random.choice(['中国银行', '中国工商银行', '中国农业银行',
    #                                 '中国建设银行', '中国交通银行', '招商银行', '民生银行'])
    #         c.bankAccount = '1234567890'
    #     c.address = '丹凤路%s号' % random.randint(1, 2000)
    #     c.contact = '联系人-%s' % i
    #     c.username = list(cxs)[i]
    #     c.telephone = '138' + ''.join([str(random.randint(0,9)) for _i in range(8)])
    #     c.save()
    
    # materials = Material.objects.all()
    # companies = Company.objects.all()
    # for i in range(ORDER_NUM):
    #     o = Order()
    #     o.company = random.choice(list(companies))
    #     o.date = datetime.datetime.now()-datetime.timedelta(days=random.randint(1, 500))
    #     o.content = '内容-%s' % i
    #     o.quantity = random.randint(1, 5)
    #     o.taxPercent = (random.choice(Order.ORDER_TAX))[0]
    #     if i % 4:
    #         o.type = Order.ORDER_TYPE[0][0]
    #         o.price = random.randint(10, 100)*50
    #     else:
    #         o.type = Order.ORDER_TYPE[1][0]
    #         o.material = random.choice(list(materials))
    #         o.sizeWidth = random.randint(1, 5)
    #         o.sizeHeight = random.randint(1, 5)
    #     o.author = random.choice(ops)
    #     o._autoFill()
    #     o.checkout = random.choice([True, False, False])
    #     o.save()
        
#     permissions = Permission.objects.all()
#     print [i.name for i in permissions]
#     print [i for i in permissions]
