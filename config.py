#-*- coding:utf-8 -*-

from fabric.api import *

env.user = 'root'
env.roledefs = {
    'local' : ['127.0.0.1'],
    'deploy1'  : [''],
    'deploy2'  : ['']
}

#服务部署目录
deploy_dir = {
    'local': '/home/test/deploy',
    'deploy1':'/home/test/deploy1',

}
#所有代码存放目录(本地)
code_dir = '/tmp/program'
project_tar_dir = '/tmp/program_tar'

#远程服务器目录
long_range_dir = '/tmp'

#url,%s为项目名称
url = 'git@github.com:haozhixin/%s.git'

#common目录(打包到本地的目录)
common_dir = '/tmp/program/common/src/common'
