#!/usr/bin/python
# -*- coding:utf-8 -*-

import os,sys,shutil
import subprocess
from config import *


#git目录是否可以正常使用
def get_branches(git_dir):
    try:
        os.chdir(git_dir)
        git_srt = subprocess.check_output(["git", "branch"])
        branches = git_srt.split('\n')
        branches_list = []
        for branch in branches[0:-1]:
            #使用str的lstrip方法将字符串的前的空格和当前branch前的“*”标记去除
            branches_list.append(branch.lstrip('* '))
        return branches_list
    except Exception,error:
        return error

#检查本地代码目录是否可以正常使用
def check_codedir(project):

    if os.path.exists(code_dir) == False:
        print '创建存放代码目录: %s'%code_dir
        os.mkdir(code_dir)
    if os.path.exists(project_tar_dir) == False:
        print '创建存放代码压缩包目录: %s'%project_tar_dir
        os.mkdir(project_tar_dir)
    #检查project是否可以进行git操作
    project_dir = os.path.join(code_dir,project)
    git_branch_status = get_branches(project_dir)
    for brach_name in git_branch_status:
        if brach_name == 'master':
            print '代码目录: %s '%project_dir
            print '分支名称为: %s'%brach_name
            return 'OK'
        elif brach_name == 2:
            return 'NO'

#更新本地的程序目录
def local_update_code(project):
    project_dir = os.path.join(code_dir,project)
    git_url = url%project
    git_status = check_codedir(project)
    try:

        if git_status == 'OK':
            print '代码更新中......'
            os.chdir(project_dir)
            subprocess.check_output(['git', 'fetch'])
            print 'Update Finished .'
        elif git_status == 'NO':
            os.chdir(code_dir)
            subprocess.check_output(['git', 'clone', git_url])
            print 'Clone Finished.'
    except Exception,error:
        print error

#压缩程序目录到/tmp/program_tar
def local_pack(project):
    if project != 'common':
        print '打包中。。。。'
        tar_name = '{0}/{1}.tar.gz'.format(project_tar_dir,project)
        tar_dir_name = os.path.join(code_dir, project, 'src')
        temporary_dir = os.path.join(project_tar_dir,project)
        if os.path.exists(temporary_dir) == False:
            os.mkdir(temporary_dir)
        #拷贝要上线的程序
        os.system('cp -r %s/** %s'%(tar_dir_name,temporary_dir))
        user_input = raw_input('是否将common包写入到要上线的程序 (y/n)')
        if user_input == 'y':
            os.system('cp -r %s %s'%(common_dir,temporary_dir))
            print '已将common 拷贝到 %s'%temporary_dir
        #切换目录
        os.chdir(temporary_dir)
        os.system('tar -zcf %s .'%(tar_name))
        print '清理临时目录: %s'%temporary_dir
        shutil.rmtree(temporary_dir)
        print '压缩包路径: %s\n'%tar_name +'打包完成。'
        return tar_name
    else:
        print project + '不能独立打包，更新一下就行了'



if __name__ == '__main__':
    project = sys.argv[1]
    local_update_code(project)
    local_pack(project)
