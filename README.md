# sparrow_django_common
>sparrow的公用模块，主要包含各种通用中间件

## 权限验证中间件


#### 一、配置"dev"环境的支持
> 提示：dev 环境下， 需要将权限验证服务转发到本地。

> 1、权限验证服务转发到本地运行, 编辑项目下的 'dev.sh' 脚本， 添加：

```sparrow-permissioin=$(kubectl get pod -n default |grep sparrow-permissioin -m 1|awk '{print "kubectl port-forward " $1 " 8001:8001 -n default"}')```
 
  
> 2、 在终端运行dev.sh ,将服务转发到本地

#### 二、配置中间件需要的参数
> 将以下参数添加到settings.py 

```
PERMISSION_MIDDLEWARE = {
    # 权限验证服务的配置
    "PERMISSION_SERVICE":{
        "name": "sparrow-permission-svc", #服务名称（k8s上的服务名）
        "host": "127.0.0.1", #IP
        "port": 8001, # 服务端口
        "address": "api/sparrow_permission/i/isassigned/", # url
    },
    # consul服务的配置
    "CONSUL": {
        "host": "127.0.0.1", # ip
        "port": 8500, # 端口
    },
    "FILTER_PATH" : [''], # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
    "METHOD_MAP" : ('PUT', 'DELETE',) # 兼容阿里请求方式中间件配置， 保持默认的即可
}
```
> 描述
 - PERMISSION_MIDDLEWARE : 中间件配置
   -  PERMISSION_SERVICE ：权限验证配置
        - name : 服务名称（k8s上的服务名）
        - host : 主机地址
        - port : 服务端口
        - address : 权限服务的path
   -  CONSUL :  consul服务的配置
        - host : 主机地址
        - port : 端口
   -  FILTER_PATH : [] ,使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
   -  METHOD_MAP : ('PUT', 'DELETE',)  兼容阿里请求方式中间件配置， 保持默认的即可

#### 三、注册中间件
> 将中间件注册到 MIDDLEWARE_CLASSES:
```
    'sparrow_django_common.middleware.permission_middleware.PermissionMiddleware'，#权限中间件
    'sparrow_django_common.middleware.methodconvert.MethodConvertMiddleware' # 兼容阿里请求方式中间件
```
















