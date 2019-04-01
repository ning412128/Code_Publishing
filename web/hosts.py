from django.shortcuts import render,redirect, HttpResponse
from .host_from import HostForm
from django.http import JsonResponse
from .models import Host
from django.template.response import TemplateResponse
def hostall(request):
    name=request.GET.get('table_search','')
    hostall=Host.objects.filter(name__contains=name)
    return TemplateResponse(request,'hostall.html',{"page_title":"主机列表",'hosts':hostall})


def createhost(request,pk=0):
    host=Host.objects.filter(pk=pk).first()
    hostfrom=HostForm(instance=host)
    if request.method=="POST":
        hostfrom = HostForm(request.POST,instance=host)
        if hostfrom.is_valid(): # 数据是否通过校验
            hostfrom.save() # 保存数据到数据库
            return JsonResponse({'status':0,'msg':'添加成功'})
        else:
            return JsonResponse({'status':1,'msg':'添加失败{}'.format(hostfrom.errors)})
    return render(request,'host_create.html',{'form':hostfrom,'pk':pk})


def del_host(request,pk):
    Host.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '添加成功'})


### 作业
# 1.实现用户的增删改查
# 2.主机的增删改查
# 3.实现项目的增删改查
    # 可以使用模态框
    #  也可以使用a标签来做
# 4.搜索需要跟分页做结合