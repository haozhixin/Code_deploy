##Code_deploy 
Problem solving:

1. code local update
2. The code is pushed to the server that needs to be on the line.
3. code roll back

## Need to install the software package:

```java
pip install fabric
```
##use a method：

* config.py, example

```java
env.roledefs = {
        'local' : ['127.0.0.1'],
        'deploy1'  : [''],
        'deploy2'  : ['']
}

```
### Execute the following command to deploy the code directly.

* python deploy-noline.py {project name}

### Code Roll Back 
* python deploy-noline.py {project name} revert
* 

### project rely install
* Configuration dependent path on config.sh :setup_file=setup.sh
* setup.sh rely format
