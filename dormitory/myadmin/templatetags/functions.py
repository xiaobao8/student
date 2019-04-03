from django import template
from django.utils.html import format_html
register = template.Library()
from myadmin import models



# 分页
@register.simple_tag
def pageShow(count,request):
    count = int(count)
    try:
        p = int(request.GET.get('p', 1))
    except:
        p = 1
    begin = p - 4
    end = p + 5
    if p < 5:
        begin = 1
        end = 10
    if count < 10:
        begin = 1
        end = count
    if p > count - 5:
        begin = count - 9
        end = count
    if begin < 1:
        begin = 1
    st = get_path(request,"p")
    path = request.path
    """
                    
                    
                    <li><a href="#">2</a></li>
                    <li><a href="#">3</a></li>
                    <li><a href="#">4</a></li>
                    <li><a href="#">5</a></li>
                    
    """


    sts = ''
    if p > 1:
        sts+='<li><a href="{}?{}p={}">«</a></li>'.format(path,st,p-1)

    for i in range(begin,end+1):
        if p == i:
            # 如果有地址
            sts += '<li  class="am-disabled"><a style="background-color:#0e90d2;color:#fff"  href="{}?{}p={}">{}</a></li>'.format(path,st,i, i)
        else:
            sts+='<li><a href="{}?{}p={}">{}</a></li>'.format(path,st,i, i)
    if p < end:
        sts+='''
                 <li><a href="{}?{}p={}">»</a></li>
        '''.format(path,st,p+1)
    return format_html(sts)

# 地址拼接
def get_path(request,org):
    # 获取当前路径  拼接地址
    get_paths = request.GET.dict()
    st = ""
    for k, v in get_paths.items():
        if k != org and k != "p":
            st += k + "=" + v + "&"
    return st