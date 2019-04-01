from django.shortcuts import render
from django.http import JsonResponse
from .models import Command,Host
from django.template.response import TemplateResponse
from utils.ansible2.runner import AdHocRunner, CommandRunner, PlayBookRunner
from utils.ansible2.inventory import Inventory
import json

def commall(request):
    if request.account.isAdmin=="0":
        comall=Command.objects.all()
    else:
        comall = Command.objects.filter(user=request.account)
    return TemplateResponse(request, 'comall.html', {"page_title": "命令列表", 'coms': comall})

def createcommand(request):
    """
    var zNodes = [
    {id: 1, pId: 0, name: "随意勾选 1", open: true},
    {id: 11, pId: 1, name: "随意勾选 1-1"},
    {id: 12, pId: 1, name: "随意勾选  1-2"},
    ];
    host_data = [
        {
            "hostname": "10.0.0.142",
            "ip": "10.0.0.142",
            "port": 22,
            "username": "root",
        },
    ]
    inventory = Inventory(host_data)
    runner = CommandRunner(inventory)

    res = runner.execute('pwd', 'all')
    # print(res.results_command)
    print(res.results_raw)
    :param request:
    :return:
    """
    hosts = Host.objects.all()
    host_list = [{"id": 1, "pId": 0, "name": "机器列表", "open": "true"}, ]
    for h in hosts:
        host_list.append({"id": h.hostip, "pId": 1, "name": h.hostip})
    if request.method == "POST":
        node = request.POST.getlist('node_ips[]')  # 获取前端传过来的列表数据
        command = request.POST.get('command')
        hosts = Host.objects.filter(hostip__in=node)
        host_data = [{'hostname': h.hostip, 'ip': h.hostip, 'port': h.ssh_port, } for h in hosts]
        inventory = Inventory(host_data)
        runner = CommandRunner(inventory)
        res = runner.execute(command, 'all')
        Command.objects.create(user=request.account,hosts_list=json.dumps(node),result=res.results_raw,command=command)
        return JsonResponse({'status': 0, "msg": "执行成功", 'data': res.results_raw})
    return render(request, 'comm_create.html', {'page_title': "新增命令", "hosts": host_list})


def detail_com(request,pk):
    detail_com=Command.objects.filter(pk=pk).first()
    print(detail_com['result'],type(detail_com['result']))
    return TemplateResponse(request,'command_detail.html',{'res':detail_com})
