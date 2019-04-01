from .cron_from import CronForm
from django.http import JsonResponse
from .models import Cron
from django.template.response import TemplateResponse
from utils.ansible2.runner import AdHocRunner
from utils.ansible2.inventory import Inventory
from django.shortcuts import reverse

def cronall(request):
    name = request.GET.get('table_search', '')
    cronall = Cron.objects.filter(name__contains=name)
    return TemplateResponse(request, 'cronall.html', {"page_title": "项目列表", 'crons': cronall})


def createcron(request, pk=0):
    cron = Cron.objects.filter(pk=pk).first()
    cronfrom = CronForm(instance=cron)
    if request.method == "POST":
        cronfrom = CronForm(request.POST, instance=cron)
        if cronfrom.is_valid():
            cronfrom.instance.create_user = request.account
            cronfrom.instance.time = " ".join(request.POST.getlist('time'))

            # 可以有两种方式
            # 第一种方式 ansible可以执行
            host_data = [{'hostname': h.hostip, 'ip': h.hostip, 'port': h.ssh_port, } for h in
                         cronfrom.cleaned_data["host"]]
            inventory = Inventory(host_data)
            runner = AdHocRunner(inventory)
            time = request.POST.getlist('time')
            tasks = [
                {"action": {"module": "cron",
                            "args": "minute={} day={} hour={} month={} weekday={} job={} name={} user={}".format(
                                time[0], time[1], time[2], time[3], time[4], cronfrom.cleaned_data['job'],
                                cronfrom.cleaned_data['name'], cronfrom.cleaned_data['user'])}, "name": "crontab"}
            ]
            ret = runner.run(tasks)
            if not ret.results_raw["ok"]:
                print(ret.results_raw)
                return JsonResponse({"status": 1, "msg": "添加失败{}".format(ret.results_raw)})
            # 第二种方式 celery可以执行 +django的时候 django-celery-beat
            cronfrom.save()
            return JsonResponse({"status": 0, "msg": "添加成功"})
        else:
            return JsonResponse({"status": 1, "msg": "添加失败{}".format(cronfrom.errors)})
    if cron:
        cron=cron.time.split(" ")
        print(cron)
    if request.path_info.startswith(reverse('createcron')):
        page_title="添加计划任务"
    else:
        page_title="编辑计划任务"
    return TemplateResponse(request, 'cron_create.html',
                            {'form': cronfrom, 'pk': pk, "page_title": page_title, 'time': cron})


def del_cron(request, pk):
    cron=Cron.objects.filter(pk=pk).first()
    host_data = [{'hostname': h.hostip, 'ip': h.hostip, 'port': h.ssh_port, } for h in
                 cron.host.all()]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    tasks = [
        {"action": {"module": "cron",
                    "args": "name={} user={} state=absent".format(cron.name, cron.user)}, "name": "crontab"}
    ]
    ret = runner.run(tasks)
    cron.delete()
    return JsonResponse({'status': 0, 'msg': '删除成功'})
