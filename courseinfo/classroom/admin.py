from django.contrib import admin

from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course


class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('campus', 'name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'name', 'classroomType', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']

admin.site.register(Campus, CampusAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Classroom, ClassroomAdmin)
