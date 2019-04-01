from django.shortcuts import render
from .team_from import TeamForm
from django.http import JsonResponse
from .models import Team
from django.template.response import TemplateResponse
from utils.gitfile import GitClass

def teamall(request):
    name=request.GET.get('table_search','')
    teamall=Team.objects.filter(name__contains=name)
    return TemplateResponse(request,'teamall.html',{"page_title":"项目列表",'teams':teamall})


def createteam(request,pk=0):
    team=Team.objects.filter(pk=pk).first()
    teamfrom=TeamForm(instance=team)
    if request.method=="POST":
        teamfrom = TeamForm(request.POST,instance=team)
        if teamfrom.is_valid(): # 数据是否通过校验
            teamfrom.save() # 保存数据到数据库
            GitClass(teamfrom.cleaned_data['name']).is_gitdir(teamfrom.cleaned_data['git_path'])
            return JsonResponse({'status':0,'msg':'添加成功'})
        else:
            return JsonResponse({'status':1,'msg':'添加失败{}'.format(teamfrom.errors)})
    return TemplateResponse(request,'team_create.html',{'form':teamfrom,'pk':pk,"page_title":"项目列表",})


def del_team(request,pk):
    Team.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 0, 'msg': '添加成功'})

def detail_team(request,pk):
    team=Team.objects.filter(pk=pk).first()
    return TemplateResponse(request,'team_detail.html',{'team':team,"page_title":"项目详情"})
### 作业
# 1.实现用户的增删改查
# 2.主机的增删改查
# 3.实现项目的增删改查
    # 可以使用模态框
    #  也可以使用a标签来做
# 4.搜索需要跟分页做结合