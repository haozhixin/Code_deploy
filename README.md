##Code_deploy 本项目概论？
本项目解决的问题：

1. 代码本地更新
2. 代码推到需要上线的服务器上
3. 回滚功能

## 需要安装的软件：

```java
pip install fabric
```
##代码使用方法：

* 需要定义的都在config.py里面,下面是举例

```java
env.roledefs = {
        'local' : ['127.0.0.1'],
        'deploy1'  : [''],
        'deploy2'  : ['']
}

```
### 执行下面命令就可以直接部署代码了
* python deploy-noline.py {项目名称}
