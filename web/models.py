from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser

# Create your models here.
status = (
    ("0", "等待更新"),
    ("1", "更新中"),
    ("2", "等待测试"),
    ("3", "测试通过"),
    ("4", "更新完成"),
    ("5", "更新失败"),
    ("6", "回滚成功"),
    ("7","回滚失败")
)


class Team(models.Model):
    Language = (
        ("0", 'python'),
        ("1", "java"),
        ("2", 'go'),
        ("3", "php"),
        ("4", "html")
    )
    name = models.CharField(verbose_name='项目名', max_length=200, unique=True)
    user_id = models.ManyToManyField('UserProfile', related_name='研发人员', verbose_name="研发人员")
    test_user = models.ManyToManyField('UserProfile', related_name='测试人员', verbose_name="测试人员")
    path = models.CharField(verbose_name='项目目录', max_length=200)
    git_path = models.CharField(verbose_name='git地址', max_length=200)
    nginxhost = models.ManyToManyField('Host', verbose_name='nginx机器', related_name="nginx", )
    nginxconf = models.CharField(verbose_name='nginx配置文件', max_length=200, null=True, blank=True)
    nginxupstream = models.CharField(verbose_name='nginx upstream名称', max_length=200, null=True, blank=True)
    host = models.ManyToManyField('Host', verbose_name='后端主机', related_name="upstarm机器")
    language = models.CharField(verbose_name='语言', choices=Language, default="0", max_length=20)
    domain=models.CharField(verbose_name='域名',null=True,blank=True,max_length=100)
    note = models.CharField(verbose_name='备注信息', max_length=218, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ("-create_time",)

    def __str__(self):
        return self.name


class Host(models.Model):
    Seetings = (
        ("0", '开发'),
        ("1", "测试"),
        ("2", "准生产"),
        ("3", "生产")
    )
    Type = (
        ("0", "nginx"),
        ("1", "other")
    )
    name = models.CharField(verbose_name="主机名", max_length=200, unique=True)
    hostip = models.GenericIPAddressField(verbose_name='主机ip地址')
    settings = models.CharField(
        verbose_name='环境',
        choices=Seetings,
        default="0", max_length=20)
    type = models.CharField(verbose_name="类型", choices=Type, default="1", max_length=20)
    ssh_port=models.CharField(verbose_name="ssh端口",default=22,max_length=10)

    def __str__(self):
        return self.hostip


class Issue(models.Model): #更新表
    team = models.ForeignKey(Team, verbose_name='发布项目')
    user = models.ForeignKey("UserProfile", verbose_name='发布人')
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    type = models.CharField(verbose_name='更新类型', choices=(("0", "文件"), ("1", "git")), default="0", max_length=20, )
    status = models.CharField(verbose_name='更新状态', choices=status, default="0", max_length=20)
    backup = models.CharField(verbose_name='备份状态', choices=(("0", "是"), ("1", "否")), default="0", max_length=20)
    path = models.CharField(verbose_name='备份文件路径', max_length=2048, null=True, blank=True)
    src_path = models.CharField(verbose_name='上传文件路径', max_length=2048, null=True, blank=True)

    class Meta:
        ordering = ['-create_time']


class Host_Issue(models.Model): #主机的更新信息表
    team = models.ForeignKey(Team, verbose_name='发布项目')
    host = models.ForeignKey(Host, verbose_name='发布机器')
    issue = models.ForeignKey(Issue, verbose_name='更新')
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(verbose_name='更新状态', choices=status, default="0", max_length=20)

    class Meta:
        ordering = ['-create_time']


class Command(models.Model):
    command = models.CharField(verbose_name="命令", max_length=200)
    result = models.CharField(verbose_name="结果", max_length=2000)
    hosts_list=models.CharField(verbose_name="执行机器", max_length=20000)
    user=models.ForeignKey('UserProfile',verbose_name='用户')
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

class UserProfile(models.Model):
    name = models.CharField(verbose_name="用户名称", max_length=200)
    email = models.CharField(verbose_name="邮箱地址", max_length=200)
    password = models.CharField(verbose_name="密码", max_length=200)
    role = models.CharField(verbose_name='角色', choices=(("0", "开发"), ("1", "测试"), ("2", '运维')), default="0",
                            max_length=10)
    isAdmin = models.CharField(verbose_name='管理员', choices=(("0", "Admin"), ("1", "普通")), default="1",
                            max_length=10)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    phone=models.CharField(verbose_name='手机号',blank=True,null=True,max_length=11)
    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Cron(models.Model):
    name = models.CharField(verbose_name="计划名称", unique=True, max_length=64)
    note = models.CharField(verbose_name="计划描述", null=True, blank=True, max_length=256)
    host = models.ManyToManyField(Host, verbose_name="任务机器", max_length=500)
    user = models.CharField(verbose_name="执行用户", null=True, blank=True, default='root', max_length=256)
    job = models.CharField(verbose_name="计划", max_length=64)
    time = models.CharField(verbose_name="计划任务执行的时间", max_length=64)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, verbose_name="创建者")

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name
