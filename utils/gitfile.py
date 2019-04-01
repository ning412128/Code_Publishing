# 获取git分支
#获取分支的提交信息
#获取所有tag
#根据分支+提交信息更新
#根据tag更新
import os
from git import Repo as ppo
from git import Git as pgit
import subprocess
class GitClass:
    def __init__(self,path):
        self.path=os.path.join("/update/git",path)

    def is_gitdir(self,url):
        if os.path.exists(self.path):
            os.makedirs(self.path)
        path=os.path.join(self.path,".git")
        if os.path.isdir(path):
            return True
        else:
            ppo.clone_from(url,self.path)
            return False
    def branch(self):
        #refs保存的是远程仓库的所有的信息，包括分支信息，包括tag
        return [str(b).split("/")[1] for b in ppo(self.path).remote().refs if str(b)!="origin/HEAD"]
    def tags(self):
        return [str(b) for b in ppo(self.path).tags]
    def chekout(self,bra):
        ab=ppo(self.path).active_branch #获取当前的分支名称
        subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path,ab)) #强制将本地分支与远程分支同步
        pgit(self.path).checkout(bra)#切换分支的时候，本地可以不存在该分支，但是远程仓库必须有本分支信息
    def commits(self,bra):
        self.chekout(bra)
        return [{"message":commit.message,"id":commit.hexsha}for commit in ppo(self.path).iter_commits()]
    def update(self,bra,type,commit=None):
        self.chekout(bra)
        if type!="tag":
            ppo(self.path).index.reset(commit=commit,head=True)
    def get_branch(self):
        print(ppo(self.path).active_branch)
