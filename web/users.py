from django.shortcuts import render,redirect, HttpResponse
from .users_from import UserForm
from django.http import JsonResponse
from .models import UserProfile
from django.template.response import TemplateResponse
def userall(request):
    name=request.GET.get('table_search','')
    userall=UserProfile.objects.filter(name__contains=name)
    return TemplateResponse(request,'userall.html',{"page_title":"用户列表",'users':userall})


def createuser(request,pk=0):
    user=UserProfile.objects.filter(pk=pk).first()
    userfrom=UserForm(instance=user)
    if request.method=="POST":
        userfrom = UserForm(request.POST,instance=user)
        if userfrom.is_valid(): # 数据是否通过校验
            userfrom.save() # 保存数据到数据库
            return JsonResponse({'status':0,'msg':'添加成功'})
        else:
            return JsonResponse({'status':1,'msg':'添加失败{}'.format(userfrom.errors)})
    return render(request,'user_create.html',{'form':userfrom,'pk':pk})


def del_user(request,pk):
    UserProfile.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '添加成功'})


### 作业
# 1.实现用户的增删改查
# 2.主机的增删改查
# 3.实现项目的增删改查
    # 可以使用模态框
    #  也可以使用a标签来做
# 4.搜索需要跟分页做结合