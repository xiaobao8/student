"""hospital URL Configuration

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
from home import views

urlpatterns = [
    # 前台首页
    url(r'^$', views.index,name="home_index"),
    # 医生详情页
    url(r'^info/(?P<pk>\d+)/$', views.actor_info,name="home_actorinfo"),

    # 登录
    url(r'^login/$', views.login,name="home_login"),
    # 注册
    url(r'^register/$', views.register,name="home_register"),
    # 退出
    url(r"^out/$", views.loginout, name="home_out_login"),

    # 个人中心
    url(r'^onemessage/$', views.one_message,name="home_one_message"),
    # ajax获取医生
    url(r'^getactor/$', views.office_actor,name="home_office_actor"),
    # ajax获取医生出诊时间
    url(r'^getactorout/$', views.actor_out,name="home_actor"),

    # 预约管理
    url(r'^order/$', views.order,name="home_order"),
    # ajax生成预约记录
    url(r"^order/ajax/$", views.ajax_order, name="home_ajax_order"),

    # 评价
    url(r"^comment/(?P<pk>\d+)/$", views.comment, name="home_comment"),


]
