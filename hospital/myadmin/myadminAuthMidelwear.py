# coding=utf-8
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import redirect
import logging
from myadmin import models
class MyadminAuthMiddleware(MiddlewareMixin):
    path = ['/myadmin/login/']
    actor_path = ["/myadmin/docrot/info/", "/myadmin/order/", "/myadmin/order/success/", "/myadmin/myadmin/out/login","/myadmin/login/"]
    def process_request(self, request):
        if request.session.get("User", None):
            if request.session["User"]["phone"] != "admin" and "myadmin" in request.path:
                if request.path not in self.actor_path and "/myadmin/order/jie/" not in request.path:
                    return HttpResponse(status=403)
        else:
            if "myadmin" in request.path:
                if request.path not in self.path:
                    return HttpResponse("<script>alert('请登录!'); location.href='/myadmin/login'</script>")