from django.db import models

class Campus(models.Model):
    name = models.CharField(verbose_name='校区', max_length=16, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)
    name = models.CharField(verbose_name='教学楼名称', max_length=16, null=True, blank=True)

    def __unicode__(self):
        return self.name

class ClassroomType(models.Model):
    name = models.CharField(verbose_name='教室类型', max_length=16, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Classroom(models.Model):
    id = models.CharField(verbose_name='教室ID', max_length=16, primary_key=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    name = models.CharField(verbose_name='教室名称', max_length=16, null=True, blank=True)
    classroomType = models.ForeignKey(ClassroomType, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    id = models.CharField(verbose_name='教师ID', max_length=32, primary_key=True, blank=True)
    name = models.CharField(verbose_name='教师姓名', max_length=32, null=True, blank=True)  

    def __unicode__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(verbose_name='学期', max_length=32, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    id = models.CharField(verbose_name='ID号', primary_key=True, max_length=32, blank=True)
    name = models.CharField(verbose_name='课程名称', max_length=256, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT)
    CLASS_TIME = models.CharField(verbose_name='上课时间', max_length=32, null=True, blank=True)
    START_TIME = models.CharField(verbose_name='课程安排', max_length=32, null=True, blank=True)
    showtext = models.CharField(verbose_name='备注上课安排', max_length=256, null=True, blank=True)
    XQ = models.CharField(verbose_name='星期', max_length=32, null=True, blank=True)
    KS = models.IntegerField(verbose_name='开始的课节', default=0)
    JS = models.IntegerField(verbose_name='结束的课节', default=0)
    ZC1 = models.IntegerField(verbose_name='第几周开始课程', default=0)
    ZC2 = models.IntegerField(verbose_name='第几周结束课程', default=0)
    SJBZ = models.IntegerField(verbose_name='有无课程', default=0)

    def __unicode__(self):
        return self.name
