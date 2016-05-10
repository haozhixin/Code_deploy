# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.colors import *
from config import *
from localoperation import *
import time
import sys

now_time = time.strftime('%Y%m%d%H%M%S')


#服务重启
def restart(service):
    for i in start_script_name[service]:
        len_number = len(run('ls /etc/init.d/%s'%i,quiet=True))
        if len_number < 55:
            sudo('service %s restart' % i)
            time.sleep(1)
            sudo('service %s status' % i)

project = sys.argv[1]
@roles(project)
def deploy(project):
    time_path = '%s/%s' % (deploy_dir[project], now_time)
    #部署代码前需要把每个项目中的setup.sh文件放到部署的服务器上面
    long_setup_file = put(setup_file%project, long_range_dir)[0]
    run('chmod +x %s'%long_setup_file)
    run(long_setup_file)
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
    restart(project)
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
    restart(project)
    print green('roll back success')



def mytask():
    execute(deploy, project)

def myrevert():
    execute(Revert)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[2] == 'revert':
            print 'roll back code'
            myrevert()
        else:
            print '回滚代码请使用: revert'
            print 'python deploy-noline.py project revert'
    else:
        mytask()

