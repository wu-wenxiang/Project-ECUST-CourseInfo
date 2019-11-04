"""courseinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from classroom import views

urlpatterns = [
    path('classroom/', include('classroom.urls')),
    path('admin/', admin.site.urls),

    path('choice/<int:page>', views.choice, name="choice"),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path(r'^classromm/list/$', views.classromm_list, name="classromm_list"),
    # path(r'^schedule/list/(?P<page>\d*)?$', views.schedule_list, name="schedule_list"),
    # path(r'^romm/list/(?P<page>\d*)?$', views.romm_list, name="romm_list"),
    # path(r'^schedule/import/$', views.schedule_import, name="schedule_import"),
    # path(r'^classromm/import/$', views.classromm_import, name="classromm_import"),

    # path('building/list/', views.building_list, name="building_list"),
    # path(r'^room/list/$', views.room_list, name="room_list"),
    # path(r'^kcmc/details/$', views.kcmc_details, name="kcmc_details"),

    path('self/study/list/', views.self_study_list, name="self_study_list"),
    path('self/building/list/', views.self_building_list, name="self_building_list"),

    # path(r'^schedule/filter/$', views.schedule_filter, name="schedule_filter"),
    # path(r'^course/list/$', views.course_list, name="course_list"),

    # path(r'^classname/list/(?P<page>\d*)?$', views.classname_list, name="classname_list"),
    # path(r'^teacher/list/(?P<page>\d*)?$', views.teacher_list, name="teacher_list"),

    path('', views.index, name="index"),
]
