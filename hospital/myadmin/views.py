from django.shortcuts import render, HttpResponse, redirect
from django.http import  JsonResponse
from home import models
# Create your views here.


# 登录
def myadmin_login(request):
    if request.method == "POST":
        # 获取用户名和密码
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        if phone == "admin":
            if password == "123456":
                request.session["User"] = {"name": "admin", "phone": "admin"}
                sess_time = 180 * 60
                request.session.set_expiry(sess_time)
                return redirect("/myadmin/")
            else:
                return HttpResponse("<script>alert('手机号与密码不匹配'); window.history.go(-1)</script>")
        else:
            # 查询医生表中是否存在
            obj = models.Actor.objects.filter(phone=phone, password=password).first()
            if obj:
                request.session["User"] = {"name": obj.name, "phone": obj.phone, "id": obj.pk}
                sess_time = 180 * 60
                request.session.set_expiry(sess_time)
                return redirect("/myadmin/docrot/info/")
            else:
                return HttpResponse("<script>alert('手机号与密码不匹配'); window.history.go(-1)</script>")
    return render(request, "myadmin/login.html")
# 退出登录
def myadmin_out_login(request):
    del request.session["User"]
    return redirect("/myadmin/login/")



# 医生列表页
def doctor(request):
    # 获取所有的医生
    doctorAll = models.Actor.objects.all()

    # 姓名模糊查询
    if request.GET.get("keyword", None):
        doctorAll = doctorAll.filter(name__contains=request.GET.get("keyword"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(doctorAll, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    doctorAll = paginator.page(p)



    return render(request, "myadmin/doctor-list.html",{
        "doctorAll": doctorAll
    })
# 医生添加
def doctor_add(request):
    # 获取所有科室
    ofiiAll = models.Office.objects.all()
    if request.method == "POST":
        # 获取所有提交数据
        data = request.POST.dict()
        # 删除跨域
        data.pop("csrfmiddlewaretoken")
        if "avatar" in data:
            # 删除
            data.pop("avatar")
        # 获取头像
        avatar = request.FILES.get("avatar")
        data["age"] = int(data["age"])
        office = int(data.pop("office"))
        try:
            models.Actor.objects.create(
                **data,
                office_id=office,
                avatar=avatar
            )
            return HttpResponse("<script>alert('添加成功！');location.href='/myadmin/'</script>")
        except:
            return HttpResponse("<script>alert('添加失败！手机号已存在');window.history.go(-1)</script>")
    return render(request, "myadmin/doctor-form.html",{
        "ofiiAll": ofiiAll
    })
# 医生修改
def doctor_update(request, pk):
    # 获取当前对象
    obj = models.Actor.objects.filter(pk=pk)
    # 获取所有科室
    ofiiAll = models.Office.objects.all()
    if request.method == "POST":
        # 获取所有提交数据
        data = request.POST.dict()
        # 删除跨域
        data.pop("csrfmiddlewaretoken")
        if "avatar" in data:
            # 删除
            data.pop("avatar")
        # 获取头像
        avatar = request.FILES.get("avatar")
        data["age"] = int(data["age"])
        office = int(data.pop("office"))
        # 如果有头像就修改头像
        if avatar:
            ac = models.Actor.objects.filter(pk=pk).first()
            ac.avatar = avatar
            ac.save()
        try:
            obj.update(
                **data,
                office_id=office,
            )
            return HttpResponse("<script>alert('修改成功');location.href='/myadmin/'</script>")
        except:
            return HttpResponse("<script>alert('添加失败！手机号已存在');window.history.go(-1)</script>")




    return render(request, "myadmin/doctor-form-update.html",{
        "obj": obj.first(),
        "ofiiAll": ofiiAll
    })
# 医生删除
def doctor_del(request):
    # 获取id
    pk = int(request.GET.get("pk"))
    # 获取当前对象然后删除
    models.Actor.objects.filter(pk=pk).delete()
    return JsonResponse({"msg":"OK", "status": 999})

# 医生个人中心页面
def doctor_info(request):
    # 获取当前医生
    obj = models.Actor.objects.filter(pk=request.session["User"]["id"]).first()
    # 获取所有科室
    officeAll = models.Office.objects.all()
    return render(request, "myadmin/doctor-info.html",{
        "obj": obj,
        "ofiiAll": officeAll
    })



# 患者
def patient(request):
    # 获取所有的患者
    patients = models.Patient.objects.all()

    # 姓名模糊查询
    if request.GET.get("keyword", None):
        patients = patients.filter(name__contains=request.GET.get("keyword"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(patients, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    patients = paginator.page(p)

    return render(request, "myadmin/huanzhe.html",{
        "patients": patients
    })
# 删除患者
def patient_del(request):
    # 获取患者id
    pk = int(request.GET.get("pk"))
    # 删除
    models.Patient.objects.filter(pk=pk).delete()
    return JsonResponse({"msg": "ok", "status": 200})


# 预约申请
def order_shen(request):
    # 获取所有待预约的
    shenAll = models.Order.objects.filter(status=0).order_by("-addtime")
    # 姓名模糊查询
    if request.GET.get("keyword", None):
        shenAll = shenAll.filter(actor__name__contains=request.GET.get("keyword"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(shenAll, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    shenAll = paginator.page(p)

    return render(request, "myadmin/shen.html",{
        "shenAll": shenAll
    })
# 接受申请
def order_jie(requets):
    # 获取医生id
    actor_id = int(requets.GET.get("actor"))
    pat_id = int(requets.GET.get("pat"))
    # 修改状态
    models.Order.objects.filter(actor_id=actor_id, patient_id=pat_id).update(status=1)

    return JsonResponse({"msg":"ok", "status":200})

# 预约成功
def order_success(request):
    # 获取所有预约成功的
    successAll = models.Order.objects.filter(status=1).order_by("-addtime")
    if request.GET.get("keyword", None):
        successAll = successAll.filter(actor__name__contains=request.GET.get("keyword"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(successAll, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    successAll = paginator.page(p)

    return render(request, "myadmin/success.html",{
        "successAll": successAll
    })
# 删除成功记录
def order_success_del(request):
    # 获取id
    pk = int(request.GET.get("pk"))
    # 删除
    models.Order.objects.filter(pk=pk).delete()
    return JsonResponse({"msg": "ok", "status": 200})



# 科室列表
def office(request):
    # 获取所有科室信息
    officeAll = models.Office.objects.all()
    # 模糊查询
    if request.GET.get("keyword", None):
        officeAll = officeAll.filter(name__contains=request.GET.get("keyword"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(officeAll, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    officeAll = paginator.page(p)


    return render(request, "myadmin/keshi.html",{
        "officeAll": officeAll
    })
# 科室添加
def office_add(request):
    if request.method == "POST":
        # 获取科室名
        name = request.POST.get("name")
        # 执行添加
        try:
            models.Office.objects.create(
                name=name
            )
            return HttpResponse("<script>alert('添加成功！');location.href='/myadmin/office/'</script>")
        except:
            return HttpResponse("<script>alert('添加失败！科室已存在');window.history.go(-1)</script>")
    return render(request, "myadmin/keshi-form.html")
# 科室修改
def office_update(request, pk):
    # 获取当前科室
    obj = models.Office.objects.filter(pk=pk).first()
    if request.method == "POST":
        try:
            obj.name = request.POST.get("name")
            obj.save()
            return HttpResponse("<script>alert('修改成功！');location.href='/myadmin/office/'</script>")
        except:
            return HttpResponse("<script>alert('修改失败！科室已存在');window.history.go(-1)</script>")
    return render(request, "myadmin/keshi-form-update.html",{
        "obj": obj
    })
# 科室删除
def office_del(request):
    # 获取科id
    oid = int(request.GET.get("id"))
    # 获取科室对象然后删除
    models.Office.objects.filter(pk=oid).delete()
    return JsonResponse({"msg":"ok", "status":200})