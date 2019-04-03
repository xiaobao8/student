from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

# 患者
class Patient(models.Model):
    # 用户名
    name = models.CharField(max_length=50)
    # 用户密码
    password = models.CharField(max_length=50)
    # 手机
    phone = models.CharField(max_length=11, unique=True)
    # 年龄
    age = models.IntegerField(null=True)
    # 性别
    sex = models.CharField(max_length=1, choices=((1, '男'), (0, '女')), default="1")
    # 与医生关系
    actor = models.ManyToManyField(to="Actor")
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)


# 医生
class Actor(models.Model):
    # 医生名
    name = models.CharField(max_length=50)
    # 手机号
    phone = models.CharField(max_length=11, unique=True)
    # 密码
    password = models.CharField(max_length=225)
    # 职务
    post = models.CharField(max_length=50)
    # 职称
    engineer = models.CharField(max_length=50)
    # 年龄
    age = models.IntegerField()
    # 性别
    sex = models.CharField(max_length=1, choices=((1, '男'), (0, '女')))
    # 详细介绍
    info = models.TextField()
    # 图片
    avatar = models.FileField(upload_to="actor/img/", default="actor/img/default.jpg",
                              verbose_name="医生图片")
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)

    # 出诊时间
    out_time = models.CharField(max_length=50)

    # 与科室 关系
    office = models.ForeignKey(to="Office")


# 预约表
class Order(models.Model):
    # 医生外键
    actor = models.ForeignKey(to="Actor")
    # 患者外键
    patient = models.ForeignKey(to="Patient")
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    # 状态
    status = models.BooleanField(default=0)



# 评论表
class Comment(models.Model):
    # 评论内容
    content = models.TextField()
    # 预约表外键
    order = models.OneToOneField(to="Order")
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)


# 科室
class Office(models.Model):
    # 科室名
    name = models.CharField(max_length=10, unique=True)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)


