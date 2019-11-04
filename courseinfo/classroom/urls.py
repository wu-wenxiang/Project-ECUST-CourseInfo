from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('classroominfo/', views.campusInfo, name='campusInfo'),
    path('classroominfo/<str:campus>/', views.buildingInfo),
    path('classroominfo/<str:campus>/<str:building>/', views.classroomInfo),

    path('courseinfo/', views.courseInfo, name='courseinfo'),
    path('courseinfo/coursename/<int:page>/', views.courseNameSearch),
    path('courseinfo/teachername/<int:page>/', views.teacherNameSearch),

    # path('choice/<int:page>', views.choice, name="choice"),
    # path(r'^classromm/list/$', views.classromm_list, name="classromm_list"),
    # path(r'^schedule/list/(?P<page>\d*)?$', views.schedule_list, name="schedule_list"),
    # path(r'^romm/list/(?P<page>\d*)?$', views.romm_list, name="romm_list"),
    # path(r'^schedule/import/$', views.schedule_import, name="schedule_import"),
    # path(r'^classromm/import/$', views.classromm_import, name="classromm_import"),

    # path('building/list/', views.building_list, name="building_list"),
    # path(r'^room/list/$', views.room_list, name="room_list"),
    # path(r'^kcmc/details/$', views.kcmc_details, name="kcmc_details"),

    # path('self/study/list/', views.self_study_list, name="self_study_list"),
    # path('self/building/list/', views.self_building_list, name="self_building_list"),

    # path(r'^schedule/filter/$', views.schedule_filter, name="schedule_filter"),
    # path(r'^course/list/$', views.course_list, name="course_list"),

    # path(r'^classname/list/(?P<page>\d*)?$', views.classname_list, name="classname_list"),
    # path(r'^teacher/list/(?P<page>\d*)?$', views.teacher_list, name="teacher_list"),
]
