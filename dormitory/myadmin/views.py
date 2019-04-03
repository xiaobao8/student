from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import JsonResponse
from myadmin import models
from functools import wraps
# Create your views here.


# 函数权限判断
def func(url):
    def check_permission(fn):
        @wraps(fn)
        def inner(reqeust, *args, **kwargs):
            # 判断当前函数的权限是否在session中
            if url in reqeust.session["permission"]:
                return fn(reqeust, *args, **kwargs)
            else:
                return HttpResponse(status=403)
        return inner
    return check_permission




# 管理员 用户列表
@func("/myadmin/user/list/")
def admin_list(request):
    # 获取所有用户
    user_list = models.Users.objects.all()
    if request.GET.get("sou", None):
        # 模糊查询
        user_list = user_list.filter(name__contains=request.GET.get("sou"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(user_list, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    user_list = paginator.page(p)

    return render(request, "myadmin/html/admin/user/list.html",{
        "userlist": user_list,
    })
# 管理员  列表添加
@func("/myadmin/user/add/")
def admin_add(request):
    # 获取所有角色
    role_list = models.Role.objects.all()
    if request.method == "POST":
        if request.POST.get("name") == "admin":
            return HttpResponse("<script>alert('用户名不能为admin！');window.history.go(-1)</script>")

        try:
            # 获取注册数据
            data = request.POST.dict()
            # 删除跨域
            data.pop("csrfmiddlewaretoken")
            # 获取角色
            roles = list(map(lambda x:int(x),request.POST.getlist("role")))
            # 删除角色键
            data.pop("role")
            # 添加用户
            user = models.Users.objects.create(**data)
            # 保存角色
            user.role = roles
            # 保存
            user.save()

            return HttpResponse("<script>alert('创建成功！');location.href='/myadmin/user/list'</script>")
        except:
            return HttpResponse("<script>alert('用户名已存在！');location.href='/myadmin/user/add'</script>")
    return render(request, "myadmin/html/admin/user/add.html",{
        "rolelist": role_list,
    })
# 管理员   用户修改
@func("/myadmin/user/update/")
def admin_update(request, uid):
    # 获取修改用户
    obj = models.Users.objects.filter(pk=uid).first()
    # 获取所有角色
    rolelist = models.Role.objects.all()
    if request.method == "POST":
         # 获取所有数据
         data = request.POST.dict()
         data.pop("csrfmiddlewaretoken")
         # 获取角色
         roles = list(map(lambda x:int(x),request.POST.getlist("role")))
         # 删除角色键
         data.pop("role")
         # 修改用户
         obj.name = data["name"]
         obj.password = data["password"]
         obj.phone = data["phone"]
         # 清空用户所有角色
         obj.role.clear()
         obj.role = roles
         # 保存
         try:
             obj.save()
             return HttpResponse("<script>alert('修改成功！');location.href='/myadmin/user/list/'</script>")
         except:
             return HttpResponse("<script>alert('用户名已存在！');window.history.go(-1)</script>")



    return render(request, "myadmin/html/admin/user/update.html",{
        "obj":obj,
        "rolelist": rolelist
    })
# 管理员   用户删除
@func("/myadmin/user/del/")
def admin_del(request):
    # 获取删除用户id
    uid = request.GET.get("uid")
    # 删除
    models.Users.objects.filter(pk=int(uid)).delete()
    return JsonResponse({"meg":"OK"})



# 管理员 角色列表
@func("/myadmin/role/list/")
def rule_list(request):
    # 获取所有角色
    roles = models.Role.objects.all()
    if request.GET.get("sou", None):
        # 模糊查询
        roles = roles.filter(name__contains=request.GET.get("sou"))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(roles, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    roles = paginator.page(p)
    return render(request, "myadmin/html/admin/rule/list.html",{
        "roles":roles,
    })
# 管理员  角色添加
@func("/myadmin/role/add/")
def rule_add(request):
    # 获取所有权限
    permissions = models.Permission.objects.all()
    if request.method == "POST":
        # 获取所有数据
        data = request.POST.dict()
        # 添加
        try:
            obj = models.Role.objects.create(
                name = data["name"]
            )
            # 添加权限
            obj.permission = list(map(lambda x:int(x),request.POST.getlist("permission")))
            # 保存
            obj.save()
            return HttpResponse("<script>alert('添加成功！');location.href='/myadmin/role/list/'</script>")
        except:
            return HttpResponse("<script>alert('角色名已存在！');window.history.go(-1)</script>")
    return render(request, "myadmin/html/admin/rule/add.html",{
        "permissions": permissions
    })
# 管理员  角色修改
@func("/myadmin/role/update/")
def rule_update(request, pk):
    # 获取角色对象
    obj = models.Role.objects.filter(pk=pk).first()
    # 获取所有权限
    permissions = models.Permission.objects.all()
    if request.method == "POST":
        # 用户名
        obj.name = request.POST.get("name")
        # 修改角色
        obj.permission.clear()
        obj.permission = request.POST.getlist("permission")
        try:
            # 保存
            obj.save()
            return HttpResponse("<script>alert('添加角色成功！');location.href='/myadmin/role/list'</script>")
        except:
            return HttpResponse("<script>alert('角色已存在！');window.history.go(-1)</script>")
    return render(request, "myadmin/html/admin/rule/update.html",{
        "obj":obj,
        "permissions": permissions
    })
# 管理员  角色删除
@func("/myadmin/role/del/")
def rule_del(request):
    # 删除
    models.Role.objects.filter(pk = int(request.GET.get("rid"))).delete()
    return JsonResponse({"msg":"ok"})


# 管理员 权限列表
@func("/myadmin/url/list/")
def url_list(request):
    # 获取所有权限
    permissions = models.Permission.objects.all().order_by("-url")
    if request.GET.get("sou", None):
        # 模糊查询
        permissions = permissions.filter(name__contains=request.GET.get("sou"))
    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(permissions, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    permissions = paginator.page(p)
    return render(request, "myadmin/html/admin/url/list.html",{
        "permissions": permissions
    })
# 管理员  权限添加
@func("/myadmin/url/add/")
def url_add(reqeust):
    if reqeust.method == "POST":
        # 获取所有数据
        data = reqeust.POST.dict()
        data.pop("csrfmiddlewaretoken")
        # 添加
        try:
            models.Permission.objects.create(
                **data
            )
            # 给超级管理员添加所有权限
            ooo = models.Role.objects.filter(name="超级管理员").first()
            ooo.permission.clear()
            ooo.permission = [i["id"] for i in list(models.Permission.objects.values("id"))]
            ooo.save()
            return HttpResponse("<script>alert('添加成功！');location.href='/myadmin/url/list/'</script>")
        except:
            return HttpResponse("<script>alert('规则说明已存在！');window.history.go(-1)</script>")
    return render(reqeust, "myadmin/html/admin/url/add.html")
# 管理员  权限修改
@func("/myadmin/url/update/")
def url_update(request, pk):
    # 获取修改修改权限
    obj = models.Permission.objects.filter(pk=pk).first()
    if request.method == "POST":
        # 获取所有数据
        data = request.POST.dict()
        # 修改
        obj.name = data["name"]
        obj.url = data["url"]
        try:
            # 保存
            obj.save()
            return HttpResponse("<script>alert('修改成功！');location.href='/myadmin/url/list/'</script>")
        except:
            return HttpResponse("<script>alert('规则说明已存在！');window.history.go(-1)</script>")
    return render(request, "myadmin/html/admin/url/update.html",{
        "obj": obj
    })
# 管理员   权限删除
@func("/myadmin/url/del/")
def url_del(request):
    # 获取权限id
    pid = request.GET.get("pid")
    # 删除
    models.Permission.objects.filter(pk=int(pid)).delete()
    return JsonResponse({"msg":"删除成功"})


# 学生列表
@func("/myadmin/student/")
def student(request):
    # 获取所有学生
    students = models.Student.objects.all()
    if request.GET.get("sou", None):
        # 模糊查询
        from django.db.models import Q
        students = students.filter(
            Q(name__contains=request.GET.get("sou")) | Q(no__contains=request.GET.get("sou")) | Q(phone__contains=request.GET.get("sou")))

    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(students, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    students = paginator.page(p)
    # 上下文
    content = {'students':students}
    return render(request,'myadmin/html/student/list.html',content)
# 学生添加
@func("/myadmin/student/add/")
def student_add(request):
    storied = models.Storied.objects.all()
    # 分配数据
    context={'storied':storied}
    if request.method == "POST":
        # 获取所有数据
        data = request.POST.dict()

        # 删除跨域
        data.pop("csrfmiddlewaretoken")
        # 获取头像
        avatar = request.FILES.get("avatar", None)
        dor = data.pop("dormitory")
        dor_num = models.Dormitory.objects.filter(pk=dor).first().id
        students_num = models.Student.objects.filter(dormitory_id = dor_num).count()
        if students_num < models.Dormitory.objects.filter(pk=dor).first().num:
            # 判断头像是否存在
            if avatar:
                try:
                    # 创建
                    models.Student.objects.create(
                        **data,
                        avatar=avatar,
                        dormitory = models.Dormitory.objects.filter(pk=dor).first()
                    )
                    return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_stu')+'"</script>')
                except:
                    return HttpResponse('<script>alert("添加失败!学号已存在");location.href="'+reverse('myadmin_stu_add')+'"</script>')
            else:
                    # 删除file
                    data.pop("avatar")
                    # 创建
                    try:
                        models.Student.objects.create(
                            **data,
                            dormitory = models.Dormitory.objects.filter(pk=dor).first()
                        )
                        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_stu')+'"</script>')
                    except:
                        return HttpResponse('<script>alert("添加失败!学号已存在");location.href="' + reverse('myadmin_stu_add') + '"</script>')
        return HttpResponse("<script>alert('宿舍已满,请重新选择');history.back(-1)</script>")
    return render(request,'myadmin/html/student/add.html',context)
# 物理删除会员
@func("/myadmin/student/del/")
def student_del(request):
    # 总体捕获异常
    try:
        #根据uid获取用户对象,执行删除
        sid = request.GET.get('sid')
        # 获取用户对象
        ob=models.Student.objects.get(id=sid)
        # 执行删除
        ob.delete()
        # 加载模板
        if request.GET.get("type", None):
            return HttpResponse('<script>alert("删除成功");location.href="' + reverse('myadmin_student_shen') + '"</script>')
        return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_stu')+'"</script>')
    except:
        return HttpResponse('<script>alert("删除失败");location.href="'+reverse('myadmin_stu')+'"</script>')
# 学生修改
@func("/myadmin/student/update/")
def student_edit(request,sid):
    # 获取所有的楼层
    storied = models.Storied.objects.all()
    #根据uid获取用户对象
    ob=models.Student.objects.get(id = sid)
    # 获取当前的所有宿舍
    sushe = ob.dormitory.storied.dormitory_set.order_by("number")
    # 分配数据
    content={'storied':storied,"sinfo":ob,"sushe":sushe}
    #判断请求方式
    if request.method=="GET":
        #显示编辑表单
        return render(request,'myadmin/html/student/edit.html',content)
    elif request.method == "POST":
        # 获取前段页面发送的数据
        data = request.POST.dict()
        # 删除宿舍键
        dor = data.pop("dormitory")
        # 获取当前宿舍id
        dor_num = models.Dormitory.objects.filter(pk=dor).first().id
        # 获取当前宿舍的人数
        students_num = models.Student.objects.filter(dormitory_id = dor_num).count()
        # 如果小于容纳人数则添加
        if students_num < models.Dormitory.objects.filter(pk=dor).first().num:
            ob.name =request.POST.get('name')
            ob.no =request.POST.get('no')
            ob.phone=request.POST.get('phone')
            ob.password=request.POST.get('password')
            ob.sex=request.POST.get('sex')
            ob.speciality=request.POST.get('speciality')
            ob.college=request.POST.get('college')
            ob.dormitory.storied_id = request.POST.get("lou")
            # 获取头像
            avatar = request.FILES.get("avatar", None)
            # 判断头像是否存在
            if avatar:
                # 头像
                ob.avatar=avatar
                ob.dormitory = models.Dormitory.objects.filter(pk=dor).first()
                # 保存
                try:
                    ob.save()
                    return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_stu')+'"</script>')
                except:
                    return HttpResponse("<script>alert('添加失败!学号已存在');history.back(-1)</script>")
            else:
                ob.dormitory = models.Dormitory.objects.filter(pk=dor).first()
                # 保存
                try:
                    ob.save()
                    return HttpResponse('<script>alert("修改成功");location.href="'+reverse("myadmin_stu")+'"</script>')
                except:
                    return HttpResponse("<script>alert('添加失败!学号已存在');history.back(-1)</script>")
        return HttpResponse("<script>alert('宿舍已满,请重新选择');history.back(-1)</script>")
# 获取楼栋相关宿舍号
def storied_dor(request):
    # 获取楼栋id
    storiedid=request.GET.get('storiedid')
    # 获取该楼栋的所有宿舍
    ob = models.Storied.objects.filter(id = int(storiedid)).first().dormitory_set.all().values()
    ob = list(ob)
    ob = sorted(ob,key=lambda x:x["number"])
    return JsonResponse(ob,safe=False)





# # 员工
# def staff(request):
#     return render(request, "myadmin/html/yuangong/list.html")
# # 员工添加
# def staff_add(reqeust):
#     return render(reqeust, "myadmin/html/yuangong/add.html")


# 宿舍
@func("/myadmin/dormitory/")
def dormitory(request):
    # 获取所有宿舍信息
    dormitory_all = models.Dormitory.objects.extra(select={"path":"concat(storied_id,number)"}).order_by("path")
    if request.GET.get("sou", None):
        # 模糊查询房间号
        dormitory_all = dormitory_all.filter(number=int(request.GET.get("sou")))
    # 排序
    dormitory_all = sorted(list(dormitory_all), key=lambda x:x.storied_id,reverse=True)
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(dormitory_all, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    dormitory_all = paginator.page(p)
    return render(request, "myadmin/html/sushe/list.html",{
        "dormitory_all": dormitory_all
    })
# 宿舍添加
@func("/myadmin/dormitory/add/")
def dormitory_add(reqeust):
    # 获取所有没有管理楼层
    floors = models.Storied.objects.order_by("number")

    if reqeust.method == "POST":
        # 获取所有添加数据
        data = reqeust.POST.dict()
        # 获取楼栋
        lid = int(data["lou"])
        # 获取该楼的所有宿舍号
        dor = list(models.Storied.objects.filter(pk=lid).first().dormitory_set.values("number"))
        dor_all = [i["number"] for i in dor]
        # 判断该栋楼是否存在该宿舍号
        if int(data["number"]) in dor_all:
            return HttpResponse("<script>alert('该宿舍号已存在');window.history.go(-1)</script>")
        else:
            # 添加宿舍
            models.Dormitory.objects.create(
                number=int(data["number"]),
                num=data["num"],
                storied_id=lid
            )
            return HttpResponse("<script>alert('添加成功');location.href='/myadmin/dormitory/'</script>")
    return render(reqeust, "myadmin/html/sushe/add.html",{
        "floors": floors
    })
# 宿舍修改
@func("/myadmin/dormitory/update/")
def dormitory_update(request, did):
    # 获取当前宿舍
    obj = models.Dormitory.objects.filter(pk=did).first()
    # 获取所有楼栋
    floors = models.Storied.objects.order_by("number")
    if request.method == "POST":
        # 获取所有添加数据
        data = request.POST.dict()
        # 如果没有做任何修改
        if int(data["num"]) == obj.num and int(data["number"]) == obj.number and int(data["lou"]) == obj.storied.pk:
            return HttpResponse("<script>alert('修改成功！');location.href='/myadmin/dormitory'</script>")
        # 获取楼栋
        lid = int(data["lou"])
        # 获取该楼的所有宿舍号
        dor = list(models.Storied.objects.filter(pk=lid).first().dormitory_set.values("number"))
        # 获取所有的宿舍号
        dor_all = [i["number"] for i in dor]

        try:
            dor_all.remove(int(data["number"]))
        except:
            pass

        # 判断该栋楼是否存在该宿舍号
        if int(data["number"]) in dor_all:
            return HttpResponse("<script>alert('该宿舍号已存在');window.history.go(-1)</script>")
        else:
            # 获取当前宿舍的所有人数
            pro = obj.student_set.all().count()
            if int(data["num"]) < pro:
                return HttpResponse("<script>alert('当前宿舍有人数"+str(pro)+"');window.history.go(-1)</script>")
            # 修改
            obj.number = data["number"]
            obj.num = data["num"]
            obj.storied_id = lid
            # 保存
            obj.save()
            return HttpResponse("<script>alert('修改成功！');location.href='/myadmin/dormitory'</script>")
    return render(request, "myadmin/html/sushe/update.html",{
        "obj": obj,
        "floors": floors
    })
# 宿舍  删除
@func("/myadmin/dormitory/del/")
def dormitory_del(request):
    # 获取当前宿舍信息
    obj = models.Dormitory.objects.filter(pk=int(request.GET.get("pk"))).first()
    # 判断该宿舍是否有人
    count = obj.student_set.all().count()
    if count == 0:
        # 删除
        obj.delete()
        return JsonResponse({"msg": "OK", "status": "200","error":0})
    return JsonResponse({"msg":"OK","status":"200","error":1})

# 楼层
@func("/myadmin/floor/")
def floor(request):
    # 获取所有楼层
    data = models.Storied.objects.order_by("number")
    if request.GET.get("sou", None):
        data =  data.filter(number=request.GET.get("sou"))
        # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(data, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    data = paginator.page(p)
    return render(request, "myadmin/html/louceng/list.html",{
        "data":data
    })
# 楼层添加
@func("/myadmin/floor/add/")
def floor_add(reqeust):
    if reqeust.method == "POST":
        # 获取添加数据
        floor_data = reqeust.POST.dict()
        # 删除跨域
        floor_data.pop("csrfmiddlewaretoken")
        # 添加楼层管理
        try:
            models.Storied.objects.create(
                number=int(reqeust.POST.get("number")),
                user_id=int(reqeust.POST.get("user")),
            )
            return HttpResponse("<script>alert('添加成功！');location.href='/myadmin/floor/'</script>")
        except:
            return HttpResponse("<script>alert('楼层号已存在！');location.href='/myadmin/floor/add/'</script>")
    # 获取所有员工
    data_temp = models.Users.objects.all()
    # 筛选出没有管理楼层的员工
    data = []
    for i in data_temp:
        try:
            # 判断是否已经管理了楼层
            te = i.storied.number
        except:
            # 说明没有管理任何楼层追加到data中
            data.append(i)
    return render(reqeust, "myadmin/html/louceng/add.html",{
        "data": data
    })
# 楼层修改
@func("/myadmin/floor/update/")
def floor_update(request, fid):
    # 获取当前楼层信息
    obj = models.Storied.objects.filter(pk=fid).first()
    # 获取所有员工
    user_temp = models.Users.objects.values("storied__number","storied__id","name","id")
    # 获取没有管理楼层的
    user_list = [{"sid":i["storied__id"],"name":i["name"],"pk":i["id"]} for i in user_temp if i["storied__number"] == None]

    for i in user_list:
        print(i)
    if request.method == "POST":
        # 获取所有数据
        data = request.POST.dict()
        # 添加
        try:
            obj.number = int(data["number"])
            obj.user_id = int(data["user"])
            obj.save()
            return HttpResponse("<script>alert('修改成功'); location.href='/myadmin/floor/'</script>")
        except:
            return HttpResponse("<script>alert('楼栋号已存在');history.back(-1)</script>")
    return render(request, "myadmin/html/louceng/update.html",{
        "obj": obj,
        "user_list": user_list
    })
# 楼层删除
@func("/myadmin/floor/del/")
def floor_del(request):
    # 获取楼栋信息
    obj = models.Storied.objects.filter(pk=request.GET.get("pk")).first()
    # 获取楼栋该楼栋下的所有宿舍
    sushe = obj.dormitory_set.all().count()
    if sushe == 0:
        # 删除
        obj.delete()
        return JsonResponse({"msg": "OK", "status": "200","error":0})
    return JsonResponse({"msg": "OK", "status":"200","error":1})


# 来访
@func("/myadmin/visit/")
def visit(request):
    # 获取所有来访记录
    visitors = models.Visit.objects.all()
    if request.GET.get("sou", None):
        # 模糊查询
        from django.db.models import Q
        visitors = visitors.filter(Q(name__contains=request.GET.get("sou"))|Q(no__contains=request.GET.get("sou"))|Q(card__contains=request.GET.get("sou")))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(visitors, 10)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    visitors = paginator.page(p)
    content = {'visitors':visitors}
    return render(request, "myadmin/html/visit/list.html",content)
# 来访添加
@func("/myadmin/visit/add/")
def visit_add(request):
    if request.method == "POST":
        # 获取所有数据
        data = request.POST.dict()
        print(data,'___________________________')
        # 删除跨域
        data.pop("csrfmiddlewaretoken")
        try:
            # 创建
            print(data,'-----------------')
            models.Visit.objects.create(
                **data,
            )
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_visit')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_visit_add')+'"</script>')
    return render(request, "myadmin/html/visit/add.html")
# 来访删除
@func("/myadmin/visit/del/")
def visit_del(request,vid):
    # 总体捕获异常
    try:
        # 获取用户对象 并删除
        visitor = models.Visit.objects.filter(id = vid).delete()
        # 加载模板
        return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_visit')+'"</script>')
    except:
        return HttpResponse('<script>alert("删除失败");location.href="'+reverse('myadmin_visit')+'"</script>')





# 登录
def login(request):
    # 判断请求方式
    if request.method=="POST":
        try:
        # 判断验证码是否正确
            if request.POST['code'] != request.session['verifycode']:
                return HttpResponse('<script>alert("验证码不正确,请重新登录");history.back(-1);</script>')
            # 超级管理员通道
            if request.POST['name'] == "admin" and request.POST['password'] == "admin123456":
                # 在session中存入登录凭证
                request.session['VipAdmin'] = {"name":"admin","id":666}
                # 设置3小时的有效登录时间
                sess_time = 180 * 60
                # 设置时间
                request.session.set_expiry(sess_time)
                # 登录成功 跳转学生列表页面
                return HttpResponse('<script>alert("登录成功");location.href="' + reverse('myadmin_stu') + '"</script>')

        # 如果是员工
            if request.POST['role'] == '0':
                # 获取用户名
                name = request.POST['name']
                # 通过用户名查找用户
                ob = models.Users.objects.get(name = name)
                # 获取发送过来的密码
                password = request.POST['password']
                # 判断密码正确
                if password == ob.password:
                    # 在session中存入登录凭证
                    request.session['VipAdmin'] = {'id':ob.id, "type":"admin","name":ob.name}
                    # 设置3小时的有效登录时间
                    sess_time = 180 * 60
                    # 设置时间
                    request.session.set_expiry(sess_time)
                    # 登录成功 跳转学生列表页面
                    return HttpResponse('<script>alert("登录成功");location.href="'+reverse('myadmin_stu')+'"</script>')
                else:
                    return HttpResponse('<script>alert("用户名或密码错误");location.href="' + reverse('myadmin_login') + '"</script>')
            # 如果是学生
            else:
                # 获取学号
                no = request.POST['name']
                # 通过学号查找学生
                student = models.Student.objects.get(no = no)
                # 获取发送过来的密码
                password = request.POST['password']
                # 判断密码正确
                if password == student.password:
                    # 在session中存入登录凭证
                    request.session['VipAdmin'] = {'id':student.id, "type":"student"}
                    # 设置3小时的有效登录时间
                    sess_time = 180 * 60
                    # 设置时间
                    request.session.set_expiry(sess_time)
                    # 跳转学生信息页面
                    return HttpResponse('<script>alert("登录成功");location.href="/myadmin/student/info/?sid='+str(student.id

)+'";</script>')
        except:
            return HttpResponse('<script>alert("用户名或密码错误");location.href="'+reverse('myadmin_login')+'"</script>')
    return render(request,'myadmin/html/login.html')
# 退出
def login_out(request):
    # 删除回话记录
    del request.session["VipAdmin"]
    return HttpResponse("<script>alert('退出成功！');location.href='/myadmin/login/'</script>")


# 学生详情页
def student_info(request):
    # 获取学生id
    sid = request.GET.get('sid')
    # 获取学生对象
    student = models.Student.objects.filter(id = sid).first()
    # 分配数据
    content ={'student':student}
    # 加载模板
    return render(request,'myadmin/html/student/info.html',content)
# 退寝申请
def student_tui(request):
   # 获取学生对象
    obj = models.Student.objects.filter(pk=int(request.GET.get("pk"))).first()
    # 修改申请状态
    obj.status = 0
    obj.save()
    return JsonResponse({"msg":"ok"})
# 学生申请
def student_shen(request):
    # 获取所有的申请信息
    data = models.Student.objects.filter(status=0)
    return render(request, "myadmin/html/student/shen.html",{
        "data": data
    })

# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')