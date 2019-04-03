from django import template
from django.utils.html import format_html
register = template.Library()

# 地址拼接
def get_path(request,org):
    # 获取当前路径  拼接地址
    get_paths = request.GET.dict()
    st = ""
    for k, v in get_paths.items():
        if k != org and k != "p":
            st += k + "=" + v + "&"
    return st



# 商品分类   ---分页
@register.simple_tag
def showCatesPage(count,request):
    path = request.path
    try:
        p = int(request.GET.get('p',1))
    except:
        p=1
    begin = p-4
    end = p+5
    count = int(count)
    if p<5:
        begin = 1
        end = 10
    if count<10:
        begin = 1
        end = count
    if p>count-5:
        begin = count-9
        end = count
    if begin<1:
        begin = 1

    # {% for i in data.paginator.page_range %}
    #                <li>
    #                  <a href="?p={{i}}">{{i}}</a></li>
    #                  {% endfor %}
                  # <li>

                  #

                  # <li><a href="#">»</a></li>
    li=''
    li += '<li><a href="'+path+'?p=1">首页</a></li>'
    if p>1:
        li += '<li><a href="'+path+'?p='+str(p-1)+'">«</a></li>'
    for i in range(begin,end+1):
        if i==p:
            li+='<li class="am-active"><a href="'+path+'?p='+str(i)+'">'+str(i)+'</a></li>'
        else:
            li+='<li><a href="'+path+'?p='+str(i)+'">'+str(i)+'</a></li>'
    if p<end:
        li += '<li><a href="'+path+'?p='+str(p+1)+'">»</a></li>'
    li += '<li><a href="'+path+'?p='+str(count)+'">尾页</a></li>'

    return format_html(li)

# 主页分页
@register.simple_tag
def indexPage(count,request):
    path = request.path
    try:
        p = int(request.GET.get('p',1))
    except:
        p=1
    begin = p-4
    end = p+5
    count = int(count)
    if p<5:
        begin = 1
        end = 10
    if count<10:
        begin = 1
        end = count
    if p>count-5:
        begin = count-9
        end = count
    if begin<1:
        begin = 1

    """
          <a href=""><span class="pc">1</span></a>
    
"""

    li=''
    li += '<a href="'+path+'?p=1"><span class="pc">首页</span></a>'
    if p>1:
        li += '<a href="'+path+'?p='+str(p-1)+'"><span class="pc">«</span><</a>'
    for i in range(begin,end+1):
        if i==p:
            li+='<a  style="background:#00BFFF" href="'+path+'?p='+str(i)+'"><span class="pc">'+str(i)+'</span></a>'
        else:
            li+='<a href="'+path+'?p='+str(i)+'"><span class="pc">'+str(i)+'</span></a>'
    if p<end:
        li += '<a href="'+path+'?p='+str(p+1)+'"><span class="pc">»</span>'
    li += '<a href="'+path+'?p='+str(count)+'"><span class="pc">尾页</span></a>'

    return format_html(li)