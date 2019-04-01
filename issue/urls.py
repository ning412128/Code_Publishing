"""issue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.users import *
from web.views import *
from web.hosts import *
from web.teams import *
from web.command import *
from web.cron import *
from web.update import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^userall/$', userall, name='userall'),
    url(r'^createuser/$', createuser, name='createuser'),
    url(r'^edituser/(?P<pk>\d+)/$', createuser, name='edituser'),
    url(r'^deluser/(?P<pk>\d+)/$', del_user, name='deluser'),
    url(r'^hostall/$', hostall, name='hostall'),
    url(r'^createhost/$', createhost, name='createhost'),
    url(r'^edithost/(?P<pk>\d+)/$', createhost, name='edithost'),
    url(r'^delhost/(?P<pk>\d+)/$', del_host, name='delhost'),
    url(r'^teamall/$', teamall, name='teamall'),
    url(r'^createteam/$', createteam, name='createteam'),
    url(r'^editteam/(?P<pk>\d+)/$', createteam, name='editteam'),
    url(r'^detailteam/(?P<pk>\d+)/$', detail_team, name='detailteam'),
    url(r'^delteam/(?P<pk>\d+)/$', del_team, name='delteam'),
    url(r'^createcommand/$', createcommand, name='createcommand'),
    url(r'^comall/$', commall, name='commall'),
    url(r'^detailcom/(?P<pk>\d+)/$', detail_com, name='detailcom'),
    url(r'^cronall/$', cronall, name='cronall'),
    url(r'^createcron/$', createcron, name='createcron'),
    url(r'^editcron/(?P<pk>\d+)/$', createcron, name='editcron'),
    url(r'^delcron/(?P<pk>\d+)/$', del_cron, name='delcron'),
    url(r'^updateall/$', updateall, name='updateall'),
    url(r'^backupall/$', backupall, name='backupall'),
    url(r'gitcreate/$', gitupdate, name='gitcreate'),
    url(r'filecreate/$', fileupdate, name='fileupdate'),
    url(r'gitbranch/(?P<pk>\d+)/$', branches, name='gitbranch'),
    url(r'gittag/(?P<pk>\d+)/$', tags, name='gittag'),
    url(r'gitcommits/(?P<pk>\d+)/(?P<bra>\w+)/$', commits, name='gitcommits'),
    url(r'^detailissue/(?P<pk>\d+)/$', detail_issue, name='detailissue'),
    url(r'^updateissue/(?P<pk>\d+)/$', update, name='updateissue'),
    url(r'^succefull/(?P<pk>\d+)/$', succefull, name='succefull'),
    url(r'^updateagain/(?P<pk>\d+)/$', again_update, name='updateagain'),
    url(r'^rollback/(?P<pk>\d+)/$', backup, name='backup'),


]
