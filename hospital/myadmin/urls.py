
from django.conf.urls import url
from django.contrib import admin

from myadmin import views

urlpatterns = [

    # 登录
    url(r"^login/$", views.myadmin_login, name="myadmin_login"),
    # 退出登录
    url(r"^myadmin/out/login$", views.myadmin_out_login, name="myadmin_out_login"),

    # 医生列表
    url(r"^$", views.doctor, name="myadmin_doctor"),
    # 医生添加
    url(r"^doctor/add/$", views.doctor_add, name="myadmin_doctor_add"),
    # 医生修改
    url(r"^doctor/update/(?P<pk>\d+)/$", views.doctor_update, name="myadmin_doctor_update"),
    # 医生删除
    url(r"^doctor/del/$", views.doctor_del, name="myadmin_doctor_del"),

    # 医生详情页
    url(r"^docrot/info/$", views.doctor_info, name="myadmin_doctor_info"),

    # 科室列表
    url(r"^office/$", views.office, name="myadmin_office"),
    # 科室添加
    url(r"^office/add/$", views.office_add, name="myadmin_office_add"),
    # 科室修改
    url(r"^office/update/(?P<pk>\d+)/$", views.office_update, name="myadmin_office_update"),
    # 科室删除
    url(r"^office/del/$", views.office_del, name="myadmin_office_del"),

    # 预约申请
    url(r"^order/$", views.order_shen, name="myadmin_order_shen"),
    # 接受申请
    url(r"^order/jie/$", views.order_jie, name="myadmin_order_jie"),

    # 预约成功
    url(r"^order/success/$", views.order_success, name="myadmin_order_success"),
    # 删除
    url(r"^order/success/del/$", views.order_success_del, name="myadmin_order_success_del"),


    # 患者管理
    url(r"^patient/$", views.patient, name="myadmin_patient"),
    # 患者删除
    url(r"^patient/del/$", views.patient_del, name="myadmin_patient_del")
]

