from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from home import models

# Create your views here.
# 前台首页
# 主页
from copy import deepcopy
def index(request):

    if 'vipUser' not in request.session:
        name = ''
        phone = ''
        sex = 1
    else:
        user = models.Patient.objects.filter(id = request.session['vipUser']['id']).first()
        name = user.name
        phone = user.phone
        sex = user.sex
    office = models.Office.objects.all()
    # 复制一个 用于主页左边显示科室
    office_copy = deepcopy(office)
    if len(office_copy) > 18:
        office_copy = office_copy[:18]
    else:
        office_copy = list(office_copy)
        for i in range(18-len(office_copy)):
            office_copy.append({})
    # 获取所有医生
    actors = models.Actor.objects.all()

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(actors, 8)

    # 获取当前页码
    p = int(request.GET.get('p', 1))

    # 获取分页数据对象[{id:1},{id:2}]  [{id:3},{id:4}]
    actors = paginator.page(p)


    return render(request,'home/index.html',{"actors": actors,'office':office,'name':name,'phone':phone,'sex':sex,"office_copy":office_copy})




# 获取科室对应医生
def office_actor(request):
    office = models.Office.objects.filter(id = request.GET.get('officeid')).first()
    actor = models.Actor.objects.filter(office=office).values()
    actor=list(actor)
    return JsonResponse(actor,safe=False)
# 获取医生对应出诊时间
def actor_out(request):
    actor = models.Actor.objects.filter(id = request.GET.get('actorid')).values()
    actor=list(actor)
    return JsonResponse(actor,safe=False)

# 前台医生详情页
def actor_info(request, pk):
    # 获取当前医院对象
    obj = models.Actor.objects.filter(pk=pk).first()
    # 获取评论
    comment = models.Comment.objects.filter(order__actor_id=pk)
    # 获取当前医生与登录患者是否有申请记录
    order_obj = models.Order.objects.filter(actor_id=pk, status=0)

    return render(request,'home/actor/info.html',{
        "obj": obj,
        "order_obj": order_obj,
        "comment": comment
    })

# 前台登录页
def login(request):
    if request.method == 'POST':
        # 获取登录的数据
        data = request.POST.dict()
        # 获取用户
        user = models.Patient.objects.filter(phone=data["phone"], password=data["password"]).first()
        # 判断用户是否存在
        if user:
            # 记录登录信息
            request.session["vipUser"] = {"phone": user.phone, "username": user.name, "id": user.pk}
            # 设置3小时的有效登录时间
            sess_time = 180 * 60
            # 设置时间
            request.session.set_expiry(sess_time)
            # 成功跳转主页
            return HttpResponse("<script>alert('登录成功！');location.href='/'</script>")
        else:
            return HttpResponse("<script>alert('手机号与密码不存在！');location.href='/login/'</script>")
    return render(request,'home/login.html')
# 退出登录
def loginout(request):
    del request.session["vipUser"]
    return HttpResponse("<script>alert('退出成功！');location.href='/login/'</script>")

# 前台注册页
def register(request):
    if request.method == 'POST':
        data = request.POST.dict()
        if data['password'] != data['repassword']:
            return HttpResponse('<script>alert("两次密码输入不一致,请重新输入!");location.href="'+reverse('home_register')+'"</script>')
        data.pop('repassword')
        data.pop("csrfmiddlewaretoken")
        try:
            models.Patient.objects.create(**data)
            return HttpResponse('<script>alert("注册成功");location.href="'+reverse('home_login')+'"</script>')
        except:
            return HttpResponse('<script>alert("手机号已存在,请重新输入!");location.href="'+reverse('home_register')+'"</script>')
    return render(request,'home/register.html')


# 前台个人中心
def one_message(request):
    try:
        patient = models.Patient.objects.filter(id = request.session['vipUser']['id']).first()
        if request.method == 'POST':
            data = request.POST.dict()
            data.pop("csrfmiddlewaretoken")
            patient.name=data['name']
            patient.sex=data['sex']
            patient.age=data['age']
            patient.phone=data['phone']
            patient.password=data['password']
            patient.save()
            return HttpResponse('<script>alert("完善成功!");location.href="'+reverse('home_one_message')+'"</script>')
        return render(request,'home/messge/one_messge.html',{'patient':patient})
    except:
        return HttpResponse('<script>alert("您还没有登录,请登录!");location.href="'+reverse('home_login')+'"</script>')

# 评价
def comment(request, pk):
    # 获取医生对象
    obj = models.Order.objects.filter(pk=pk).first().actor
    if request.method == "POST":
        # 获取评论内容
        content = request.POST.get("content")
        # 提交
        models.Comment.objects.create(
            content = content,
            order_id=pk
        )
        return HttpResponse("<script>alert('感谢你的反馈！');location.href='/order/'</script>")
    return render(request, "home/messge/comment.html",{
        "obj":obj
    })

# 预约管理
def order(request):
    try:
        request.session["vipUser"]
    except:
        return HttpResponse('<script>alert("您还没有登录,请登录!");location.href="'+reverse('home_login')+'"</script>')
    patient = models.Patient.objects.filter(id = request.session['vipUser']['id']).first()
    orderlist = models.Order.objects.filter(patient=patient).order_by("-addtime")

    if not request.GET.get("status", None) or request.GET.get("status", 1) == "1":
        orderlist = orderlist.filter(status=0)
    else:
        orderlist = orderlist.filter(status=1)

    if request.method == 'POST':
        actorid = request.POST.get('actor',None)
        if not actorid:
            return HttpResponse('<script>alert("请选择医生!");location.href="'+reverse('home_index')+'"</script>')
        actor = models.Actor.objects.filter(id = int(actorid)).first()
        # 判断之前是否已经申请过了
        check_shen = models.Order.objects.filter(
            patient_id=patient.id,
            actor_id=actor.id,
            status=0
        ).first()

        if check_shen:
            return HttpResponse('<script>alert("你已预约了！请等待");location.href="'+reverse('home_order')+'"</script>')

        # 创建预约对象
        models.Order.objects.create(
            actor = actor,
            patient = patient
        )
        return HttpResponse('<script>alert("预约成功");location.href="'+reverse('home_order')+'"</script>')

    return render(request,'home/messge/order.html',{'orderlist':orderlist})

# 详情也ajax预约
def ajax_order(request):
    # 获取医生id
    aid = int(request.GET.get("pk"))
    # 生成预约记录

    models.Order.objects.create(
        actor_id=aid,
        patient_id=request.session["vipUser"]["id"]
    )
    return JsonResponse({"msg":"ok","status":200, "error": 0})


