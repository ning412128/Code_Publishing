from .update_from import GitForm, FileForm
from django.http import JsonResponse
from .models import Issue, Team, Host_Issue
from django.template.response import TemplateResponse
from utils.ansible2.runner import AdHocRunner
from utils.ansible2.inventory import Inventory
from django.shortcuts import reverse, render
from django.db.models import Q
from utils.gitfile import GitClass
import time
import os
from django.views.decorators.csrf import csrf_exempt
import random
import openpyxl


def updateall(request):
    name = request.GET.get('table_search', '')
    updateall = Issue.objects.filter(Q(user=request.account) | Q(team__test_user=request.account),
                                     team__name__contains=name)
    return TemplateResponse(request, 'issueall.html', {"page_title": "更新列表", 'updateall': updateall})


def backupall(request):
    name = request.GET.get('table_search', '')
    backupall = Issue.objects.filter(Q(user=request.account) | Q(team__test_user=request.account),
                                     team__name__contains=name, status="6")
    return TemplateResponse(request, 'issueall.html', {"page_title": "回滚列表", 'updateall': backupall})


def gitupdate(request):
    gitform = GitForm()
    if request.method == "POST":
        gitform = GitForm(request.POST)
        if gitform.is_valid():
            gitform.instance.user = request.account
            gitform.instance.type = "1"
            gitform.instance.path = str(int(time.time()))
            if request.POST.get('utype') == "bra":
                GitClass(gitform.cleaned_data['team'].name).update(request.POST.get('braname'), "bra",
                                                                   request.POST.get('bracommit'))
            else:
                GitClass(gitform.cleaned_data['team'].name).update(request.POST.get('tagname'), "tag")
            issue = gitform.save()
            host_list = gitform.cleaned_data['team'].host.all()
            for h in host_list:
                Host_Issue.objects.create(host=h, issue=issue, team=gitform.cleaned_data['team'])
            return JsonResponse({'status': 0, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败{}'.format(gitform.errors)})
    return render(request, 'git.html', {"form": gitform})


def handle_uploaded_file(f, teamname, t):
    path = "/update/file/{}/{}".format(teamname, t)
    if not os.path.exists(path):
        os.makedirs(path)
    for file in f:
        name = file.name.split(".")[1]
        if name not in ["xls", "xlsx"]:
            return False
        with open(os.path.join(path, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True


@csrf_exempt
def fileupdate(request):
    fileform = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            t = str(int(time.time()))
            form.instance.user = request.account  # 保存发布人
            form.instance.type = "0"  # 保存发布的类型
            form.instance.path = t  # 备份的路径
            team_name = form.cleaned_data['team'].name
            form.instance.src_path = "/update/file/{}/{}".format(team_name, t)
            status = handle_uploaded_file(request.FILES.getlist("file_field"), team_name, t)
            issue = form.save()  # 保存到数据库
            host_list = form.cleaned_data['team'].host.all()
            for h in host_list:
                Host_Issue.objects.create(host=h, issue=issue, team=form.cleaned_data['team'])
            if status:
                return JsonResponse({'status': 0, 'msg': '上传成功'})
            else:
                return JsonResponse({'status': 1, 'msg': '上传失败，没有上传excel表格'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败{}'.format(form.errors)})
    return render(request, "file_create.html", {"form": fileform})


def branches(request, pk):
    team = Team.objects.filter(pk=pk).first()
    g = GitClass(team.name)
    return JsonResponse({"status": 0, 'data': g.branch()})


def tags(request, pk):
    team = Team.objects.filter(pk=pk).first()
    g = GitClass(team.name)
    return JsonResponse({"status": 0, 'data': g.tags()})


def commits(request, pk, bra):
    team = Team.objects.filter(pk=pk).first()
    g = GitClass(team.name)
    return JsonResponse({"status": 0, 'data': g.commits(bra)})


def detail_issue(request, pk):
    issue = Issue.objects.filter(pk=pk).first()
    return render(request, "isuue_detail.html", {"res": issue})


def update(request, pk):
    """
    先在所有机器中随机挑选一台机器做更新，
    先从nginx上把机器摘下来，在更新服务
    去发送邮件通知测试人员做测试,
    当测试通过以后，应该把这台机器挂载到nginx上
    在更新剩余的机器
    :param request:
    :param pk:
    :return:
    """
    issue = Issue.objects.filter(pk=pk).first()  # 获取issue里面的数据
    print(issue)
    host_list = issue.host_issue_set.all()  # 获取到所有的host_issue里面的对象
    print(host_list)
    host = random.choice(host_list) #获取到所有的host_issue里面的一个对象
    # 冲nginx上把机器摘下来
    # nginx_res = nginx_server(issue.team, [host], 1)
    # 更新这台机器的服务
    # server_res = upstream_server([host], issue, issue.type)
    nginx_res = True
    server_res = True
    # 发送邮件，可以通过celery来做
    if nginx_res and server_res:
        # if server_res:
        issue.status = "2"
        issue.save()
        host.status = "2"
        host.save()
        return JsonResponse({'status': 0, 'msg': '更新完成'})
    else:
        issue.status = "5"
        issue.save()
        host_issue = Host_Issue.objects.filter(issue=issue, host=host).first()
        host_issue.status = "5"
        host_issue.save()
        return JsonResponse({'status': 1, 'msg': '更新失败'})


def nginx_server(team, host, type):
    """
    :param team: 项目
    :param host: 要下线的主机
    :return:
    """
    tasks = []
    for h in host:
        if type == 1:
            tasks.append(
                # nginx把机器下线
                {"action": {"module": "replace",
                            "args": "path={} regexp=({}.*) replace=#\\1".format(team.nginxconf, h.host.hostip)},
                 "name": "nginx_down"},
            )
        else:
            tasks.append(
                # 把机器上线
                {"action": {"module": "replace",
                            "args": "path={} regexp=#({}.*) replace=\\1".format(team.nginxconf, h.host.hostip)},
                 "name": "nginx_down"},
            )
    tasks.append({"action": {"module": "service", "args": "name=nginx state=reloaded"}, "name": "nginx_restart"})
    host_data = [{'hostname': h.hostip, 'ip': h.hostip, 'port': h.ssh_port, } for h in team.nginxhost.all()]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    ret = runner.run(tasks)
    if not ret.results_raw["ok"]:
        return False
    return True


def upstream_server(host, issue, type, status=1):
    """
    :param host:  要更新的机器
    :param issue: 当前更新的issue，有文件的地址
    :param type: 1 git 2 文件
    :param status 0回滚 1更新
    :return:
    """
    if status:
        tasks = [
            {"action": {"module": "file",
                        "args": "path=/tmp/{}/{} state=directory".format(issue.team.name, issue.path)},
             "name": "mdkirfile"},
            {"action": {"module": "shell",
                        "args": "cp -rf {} /tmp/{}/{}".format(issue.team.path, issue.team.name, issue.path)},
             "name": "backup"},
        ]
        if type == "1":
            tasks.append({"action": {"module": "copy",
                                     "args": "dest={} src=/update/git/{}/".format(issue.team.path, issue.team.name)},
                          "name": "updategit"})
        else:
            excel_path = "/update/file/{}/{}/readme.xlsx".format(issue.team.name, issue.path)
            if os.path.exists(excel_path):
                wb = openpyxl.load_workbook(excel_path)
                wb1 = wb['update']
                for r in wb1.rows():
                    tasks.append(
                        {"action": {"module": "copy",
                                    "args": "dest={} src=/update/file/{}/{}/{}".format(
                                        os.path.join(issue.team.path, r[1].value), issue.team.name, issue.path,
                                        r[0].value)},
                         "name": "updatefile"})
            else:
                return False
    else:
        # 回滚
        tasks = [{"action": {"module": "shell",
                             "args": "cp -rf /tmp/{}/{} {}".format(issue.team.name, issue.path, issue.team.path)},
                  "name": "backup"},
                 ]
    host_data = [{'hostname': h.host.hostip, 'ip': h.host.hostip, 'port': h.host.ssh_port, } for h in host]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    ret = runner.run(tasks)
    print(ret.results_raw)
    if not ret.results_raw["ok"]:
        return False
    return True


def succefull(request, pk):
    """
    先去获取获取项目
    将机器上线
    将状态改为测试通过
    :param request:
    :param pk:
    :return:
    """
    succe_issue = Issue.objects.filter(pk=pk).first()
    host_issue = succe_issue.host_issue_set.filter(status="2") #获取等待测试的数据
    # nginx_res = nginx_server(succe_issue.team, host_issue, 1)
    nginx_res = True
    if nginx_res:
        host_issue.update(status="3") #将所有查询到的数据都改成测试通过
        wait_issue = succe_issue.host_issue_set.filter(status="0") #要获取等待更新的数据
        if wait_issue:
            succe_issue.status = "3"  # 总表
            succe_issue.save()
        else:
            succe_issue.status = "4"  # 总表
            succe_issue.save()
        return JsonResponse({'status': 0, 'msg': '测试通过'})
    else:
        succe_issue.status = "5"
        succe_issue.save()
        host_issue.status = "5"
        host_issue.save()
        return JsonResponse({'status': 1, 'msg': '更新失败'})


def again_update(request, pk):
    issue = Issue.objects.filter(pk=pk).first()
    host_list = issue.host_issue_set.filter(status="0")
    # nginx_res=nginx_server(issue.team, host_list, 1)
    # 更新这台机器的服务
    # server_res = upstream_server(host_list, issue, issue.type)
    # 发送邮件，可以通过celery来做
    nginx_res = True
    server_res = True
    if nginx_res and server_res:
        issue.status = "2"
        issue.save()
        host_list.update(status="2")
        return JsonResponse({'status': 0, 'msg': '更新完成'})
    else:
        issue.status = "5"
        issue.save()
        host_list.update(status="5")
        return JsonResponse({'status': 1, 'msg': '更新失败'})


def backup(request, pk):
    issue = Issue.objects.filter(pk=pk).first()
    host_issue = issue.host_issue_set.filter(Q(status="2") | Q(status="3"))
    print(host_issue)
    server_res = True
    # server_res = upstream_server(host_issue, issue, issue.type,0)
    if server_res:
        issue.status = "6"
        issue.save()
        host_issue.update(status="6")
        return JsonResponse({'status': 0, 'msg': '回滚成功'})
    else:
        issue.status = "7"
        issue.save()
        host_issue.update(status="7")
        return JsonResponse({'status': 1, 'msg': '回滚失败'})