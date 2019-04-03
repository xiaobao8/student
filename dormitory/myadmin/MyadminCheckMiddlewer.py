# coding=utf-8
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import redirect
import logging
from myadmin import models
class MyadminAuthMiddleware(MiddlewareMixin):
   check_login = ["/myadmin/verifycode/","/myadmin/login/"]
   def process_request(self, request):
      # 未登录拦截
      if request.path not in self.check_login:
         try:
            re = request.session["VipAdmin"]["id"]
            # 如果是超级管理员
            if request.session["VipAdmin"].get("name", None) == "admin":
               # 获取所有的权限
               all_permission = list(models.Permission.objects.all().values())
               request.session["permission"] = [i["url"] for i in all_permission]
               print(request.session["permission"])
            else:
               # 如果是学生 只能访问学生详情页面
               if request.session["VipAdmin"]["type"] == "student":
                  if "/myadmin/student/info/" not in request.path and "/myadmin/student/tui/" not in request.path and "/myadmin/login/out/" not in request.path:
                     return HttpResponse(status=403)

               # 如果是管理用户
               if request.session["VipAdmin"]["type"] == "admin":
                  if "/myadmin/student/info/" in request.path:
                     return HttpResponse(status=403)
                  # 获取当前用户
                  obj = models.Users.objects.filter(pk=request.session["VipAdmin"]["id"]).first()
                  # 获取所有权限
                  permission_all = list(obj.role.values("permission__url"))
                  # 创建空集合去重URL
                  permission_set = set()

                  for i in permission_all:
                     permission_set.add(i["permission__url"])
                  # 将用户所有的权限放入session中  后续做判断
                  # print(permission_set)
                  request.session["permission"] = list(permission_set)

         except:
            return HttpResponse("<script>alert('请登录！');location.href='/myadmin/login/'</script>")
