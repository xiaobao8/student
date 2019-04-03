"""dormitory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myadmin import views

urlpatterns = [

    # 管理员  用户
    url("^user/list/$", views.admin_list, name="myadmin_list"),
    # 管理员  用户添加
    url("^user/add/$", views.admin_add, name="myadmin_add"),
    # 管理员 用户修改
    url(r"user/update/(?P<uid>\d+)/$", views.admin_update, name="myadmin_update"),
    # 管理员  用户删除
    url(r"^user/del/$", views.admin_del, name="myadmin_del"),

    # 管理员  角色
    url("^role/list/$", views.rule_list, name="myadmin_rule"),
    # 管理员  角色添加
    url("^role/add/$", views.rule_add, name="myadmin_rule_add"),
    # 管理员  修改
    url(r"^role/update/(?P<pk>\d+)/$", views.rule_update, name="myadmin_rule_update"),
    # 管理员 删除
    url(r"^role/del/$", views.rule_del, name="myadmin_rule_del"),

    # 管理员  权限
    url("^url/list/$", views.url_list, name="myadmin_url"),
    # 管理员  权限添加
    url("^url/add/$", views.url_add, name="myadmin_url_add"),
    # 管理员  权限修改
    url(r"^url/update/(?P<pk>\d+)/$", views.url_update, name="myadmin_url_update"),
    # 管理员  权限删除
    url(r"^url/del/$", views.url_del, name="myadmin_url_del"),

   # 学生管理
    url(r"^student/$", views.student, name="myadmin_stu"),
    # 学生管理  添加
    url(r"^student/add/$", views.student_add, name="myadmin_stu_add"),
    # 学生管理  删除
    url(r"^student/del/$", views.student_del, name="myadmin_stu_del"),
    # 学生管理  修改
    url(r"^student/update/(?P<sid>\d+)/$", views.student_edit, name="myadmin_stu_edit"),
    # 获取楼栋号及宿舍
    url(r"^storied/dor/$", views.storied_dor, name="myadmin_storied"),
    # 学生申请管理
    url(r"^student/shen/$", views.student_shen, name="myadmin_student_shen"),


    # # 员工管理
    # url(r"^staff/$", views.staff, name="myadmin_staff"),
    # # 学生管理  添加
    # url(r"^staff/add/$", views.staff_add, name="myadmin_staff_add"),


    # 宿舍管理
    url(r"^dormitory/$", views.dormitory, name="myadmin_dormitory"),
    # 宿舍管理  添加
    url(r"^dormitory/add/$", views.dormitory_add, name="myadmin_dormitory_add"),
    # 宿舍管理 修改
    url(r"^dormitory/update/(?P<did>\d+)$", views.dormitory_update, name="myadmin_dormitory_update"),
    # 宿舍删除
    url(r"^dormitory/del/$", views.dormitory_del, name="myadmin_dormitory_del"),


    # 楼层管理
    url(r"^floor/$", views.floor, name="myadmin_floor"),
    # 楼层管理  添加
    url(r"^floor/add/$", views.floor_add, name="myadmin_floor_add"),
    # 楼层管理 修改
    url(r"^floor/update/(?P<fid>\d+)/$", views.floor_update, name="myamdin_floor_update"),
    # 楼层删除
    url(r"^floor/del/$", views.floor_del, name="myadmin_floor_del"),

    # 来访管理
    url(r"^visit/$", views.visit, name="myadmin_visit"),
    # 来访管理  添加
    url(r"^visit/add/$", views.visit_add, name="myadmin_visit_add"),
    # 来访管理  删除
    url(r"^visit/del/(?P<vid>\d+)$", views.visit_del, name="myadmin_visit_del"),


    # 登录
    url(r"^login/$", views.login, name="myadmin_login"),
    # 退出
    url(r"^login/out/$", views.login_out, name="myadmin_login_out"),
    # 验证码
    url(r'^verifycode/$',views.verifycode,name='myadmin_verifycode'),
    # 学生信息
    url(r"^student/info/$", views.student_info, name="myadmin_studentinfo"),
    # 退寝
    url(r"^student/tui/$", views.student_tui, name="myadmin_stu_tui"),
]
