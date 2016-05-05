# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.colors import *
from config import *
from localoperation import *
import time
import sys

now_time = time.strftime('%Y%m%d%H%M%S')

project = sys.argv[1]
@roles(project)
def deploy(project):
    time_path = '%s/%s' % (deploy_dir[project], now_time)
    check_codedir(project)
    local_update_code(project)
    # 获取包名
    tar_name = local_pack(project)
    # 推到部署服务器上
    deploytarname = put(tar_name, long_range_dir)[0]
    run('mkdir -p %s' % time_path)
    run('tar -zxf %s -C %s' % (deploytarname, time_path))
    with cd(deploy_dir[project]):

        latest_name = run('ls latest', quiet=True)
        #当len小于60的时候说明latest文件不存在，old_len相同原理
        if len(latest_name) < 60:
            print 'latest文件不存在'
            run('ln -s %s latest'%now_time)
            run('ln -s %s oldversion'%now_time)
        else:
            print 'latest文件存在'
            now_name = run("ls -l latest |awk {'print $11'}")
            old_len = len(run('ls oldversion',quiet=True))
            if old_len < 60:
                print 'oldversion 目录不存在'
                # run('ln -s %s oldversion' % (now_name))
            else:
                run('rm oldversion')
            run('ln -s %s oldversion' % (now_name))
            run('rm latest')
            run('ln -s %s latest'%now_time)
    run('chown -R capitalcloud.capitalcloud %s' % deploy_dir[project])
    print green('success')

#代码回滚
@roles(project)
def Revert():
    with cd(deploy_dir[project]):
        lodversion_name = run("ls -l oldversion |awk {'print $11'}")
        if len(run('ls latest',quiet=True)) < 60:
            pass
        else:
            print '存在'
            run('rm latest')
        run('ln -s %s latest'%lodversion_name)
    run('chown -R capitalcloud.capitalcloud %s' % deploy_dir[project])
    print green('roll back success')


#执行代码部署
def mytask():
    execute(deploy, project)

#执行代码回滚
def myrevert():
    execute(Revert)

# mytask()
#myrevert()
