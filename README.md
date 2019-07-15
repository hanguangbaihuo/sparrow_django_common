# sparrow_django_common
sparrow的公用模块，主要包含各种通用中间件

##配置权限验证中间件
### 一、配置"dev"环境的支持
> 1、  将权限验证服务转发到本地运行, 编辑项目下的 'dev.sh' 脚本， 添加：
 `sparrow-permissioin=$(kubectl get pod -n default |grep sparrow-permissioin -m 1|awk '{print "kubectl port-forward " $1 " 8001:8001 -n default"}')`
 
> 2、  将权限验证服务所需要的环境变量添加到 settings.py 


```
try:
    PERMISSION_RUN_ENV = os.environ['PERMISSION_RUN_ENV']
except Exception as ex:
    raise ex
```
### 二、配置中间件需要的参数
> 1、  将以下参数添加到settings.py (权限验证服务的在各环境中的名称， 用于中间件通过名称找到权限验证服务的地址)
```
PERMISSION_SVC = {
    "pro": "pro-sparrow-permission-svc", # 线上环境权限验证服务在k8s中的名称
    "dev": "sparrow-permission-svc",  # 开发环境权限验证服务在k8s中的名称
    "test": "sparrow-permission-svc",   # 测试环境权限验证服务在k8s中的名称
    "unit": "",  # 
}
```
>2、  配置 FILTER_PATH， 如果哪些url不需要从 中间件中验证， 可以添加到FILTER_PATH 中
```
FILTER_PATH = ['' ]
```