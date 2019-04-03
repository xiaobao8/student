from django.db import models

# Create your models here.

# 用户
class Users(models.Model):
    # 用户名
    name = models.CharField(max_length=32,verbose_name="用户名",unique=True)
    # 用户密码
    password = models.CharField(max_length=255)
    # 手机号码
    phone = models.CharField(max_length=30)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    # 角色外键
    role = models.ManyToManyField(to="Role")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

# 角色
class Role(models.Model):
    # 角色名
    name = models.CharField(max_length=32,unique=True)
    # 权限外键
    permission = models.ManyToManyField(to="Permission")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 权限
class Permission(models.Model):
    # 权限名
    name = models.CharField(max_length=255,unique=True)
    # 对应URL
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 学生
class Student(models.Model):
    # 学号
    no = models.CharField(max_length=50, unique=True)
    # 用户名
    name = models.CharField(max_length=50)
    # 用户密码
    password = models.CharField(max_length=50)
    # 手机
    phone = models.CharField(max_length=11)
    # 性别
    sex = models.CharField(max_length=1, choices=((1, '男'), (0, '女')))
    # 图片
    avatar = models.FileField(upload_to="stu_img/", default="stu_img/default.png",
                              verbose_name="头像")
    # 专业
    speciality = models.CharField(max_length = 50)
    # 学院
    college = models.CharField(max_length = 50)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    # 状态  0申请中   1在寝
    status = models.BooleanField(default=1)
    # 与宿舍关系
    dormitory = models.ForeignKey(to="Dormitory")



# 宿舍
class Dormitory(models.Model):
    # 宿舍号
    number = models.IntegerField()
    # 人数
    num = models.IntegerField(default = 6)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    # 楼层外键
    storied = models.ForeignKey(to="Storied")




# 楼栋
class Storied(models.Model):
    # 楼栋号
    number = models.IntegerField(unique=True)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    # 与员工关系
    user = models.OneToOneField(to="Users")



# 来访
class Visit(models.Model):
    # 姓名
    name = models.CharField(max_length=50)
    # 学号
    no = models.CharField(max_length=50)
    # 身份证号
    card = models.CharField(max_length = 18)
    # 访问宿舍
    dormitory = models.CharField(max_length =50)
    # 创建时间
    addtime = models.DateTimeField(auto_now_add=True)
