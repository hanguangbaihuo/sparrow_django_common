# sparrow_django_common
>sparrow的公用模块，主要包含各种通用中间件

* * *

## 安装中间件
> 1. 在项目目录下新建requirements_self.txt 中添加：
```
git+https://github.com/hanguangbaihuo/sparrow_django_common.git
```
> 2. 在终端执行
```
pip install requirements_self.txt
```

* * *

## PERMISSION_MIDDLEWARE (权限验证中间件)
> 描述
```
                            (url + method + user_id)
                                        |               / 有权限则允许通过
    request -> PermissionMiddleware ---https---> 权限模块
                                                        \ 无权限则返回HTTP 403错误
```

#### 一、配置"dev"环境的支持
> 提示：dev 环境下， 需要将权限验证服务转发到本地。

> 1、权限验证服务转发到本地运行：

```
permission=$(kubectl get pods -n default | grep sparrow-permissioin -m 1 | awk '{print "kubectl port-forward "$1 " 8001:8001 -n default"}')
exec $permission &
```


#### 二、配置PERMISSION_MIDDLEWARE需要的参数
> 将以下参数添加到settings.py 

```
PERMISSION_MIDDLEWARE = {
    # 权限验证服务的配置
    "PERMISSION_SERVICE":{
        "name": "sparrow-permission-svc", #服务名称（k8s上的服务名）
        "host": "", #IP
        "port": 8001, # 服务端口, dev环境需要注意， 配置写的端口需要和转发到本地的端口保持一致
        "address": "api/sparrow_permission/i/isassigned/", # url
    },
    "FILTER_PATH" : [''], # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
    "SKIPPED": False, # 是否启用权限中间件， 不配置SKIPPED， 或者SKIPPED:True, 则跳过中间件， 如果SKIPPED:False，则不跳过中间件
}


# 权限中间件需要到consul中去发现权限服务的地址， 所以需要配置consul服务的地址
CONSUL_CLIENT_ADDR = {
    "host": "127.0.0.1",
    "port": 8500
}

RUN_ENV = "dev"  # 开发：dev, 测试：test, 正式： pro 
```

> 描述
 - PERMISSION_MIDDLEWARE : 中间件配置
   -  PERMISSION_SERVICE ：权限验证配置
        - name : 服务名称（k8s上的服务名， 必要配置）
        - host : 主机地址(非必要配置，如果配置了，则走配置中的host， 不配置从consul中查找服务)
        - port : 服务端口（必要配置）
        - address : 权限服务的path（必要配置）
   -  FILTER_PATH : [] ,使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中（非必要配置）
   -  SKIPPED : True/False   是否启用权限中间件， 不配置SKIPPED， 或者SKIPPED:True, 则跳过中间件， 如果SKIPPED:False，则不跳过中间件
   
   
-  CONSUL_CLIENT_ADDR： consul配置
   - host : 主机地址（必要配置）
   - port : 服务端口（必要配置）


-  RUN_ENV： 运行环境  （必要配置），如果不配置，开发环境会找不到PERMISSION服务

   
#### 注册 PERMISSION_MIDDLEWARE 
> 注册中间件
```
MIDDLEWARE_CLASSES = {
    'sparrow_django_common.middleware.permission_middleware.PermissionMiddleware',    #权限中间件
```

* * *
   
## METHOD_MIDDLEWARE
> 兼容阿里不支持 put/delete 请求
#### 配置METHOD_MIDDLEWARE需要的参数
> 将以下参数添加到settings.py
```
METHOD_MIDDLEWARE = {
    "METHOD_MAP": ('PUT', 'DELETE',), 
}
```
> 描述
 - METHOD_MIDDLEWARE : 中间件配置
   -  METHOD_MAP ：中间件兼容阿里云不支持put/delete请求的配置


#### 注册 METHOD_MIDDLEWARE
> 注册中间件
```
MIDDLEWARE_CLASSES = (
    'sparrow_django_common.middleware.methodconvert.MethodConvertMiddleware',      #兼容阿里请求方式中间件
)
```



* * *

## JWTMiddleware
> 描述：
```buildoutcfg

```

#### 配置 JWTMiddleware 中间件需要的参数
> 将以下参数添加到settings.py
```
JWT_MIDDLEWARE = {
    "JWT_SECRET": "问 tianyi"
}
``` 
>参数说明： JWT_SECRET : jwt_secret

#### 注册 JWTMiddleware

> 注册中间件
```
MIDDLEWARE_CLASSES = (
    'sparrow_django_common.middleware.JWT_middleware.JWTMiddleware', 
```


 * * *


 ## SparrowAuthentication

 #### 配置 SparrowAuthentication 认证需要的参数(仅兼容django2.2以上版本)

> 将以下参数添加到settings.py
```
SPARROW_AUTHENTICATION = {
    "USER_CLASS_PATH": "sparrow_django_common.common.user.User",
}
``` 
> 参数说明： USER_CLASS_PATH： 路径中的User为中间件的User模版， 可以根据自己的需求重新创建User， 并将自己的User路径按照模版格式放到：USER_CLASS_PATH下 

> 注册中间件
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'sparrow_django_common.middleware.authentication.SparrowAuthentication',
    )
}

```



* * *

## CONSUL_SERVICE  (以模块的方式使用)

#### 依赖配置， 需放到setting.py 里面
```
# consul的地址
CONSUL_CLIENT_ADDR = {
    "host": "127.0.0.1",
    "port": 8500
},

# consul服务需要知道当前开发环境，如果是开发环境， 需要发现的服务的host:prot会返回：127.0.0.1:8001
RUN_ENV = "dev"  # 开发：dev, 测试：test, 正式： pro 
```

#### 在settings中配置需要发现的服务（如使用CONSUL_SERVICE， 请使用规定的格式）
```
 SERVICE_DEPENDENCIES = {  # 名称可修改
    # 
    "SPARROW_XX_SERVICE":{  # 名称可修改
        "name": "", #服务名称（k8s上的服务名， 必要配置， 键不可修改）
        "host": "", #IP（非必要配置， 键不可修改）
        "port": 8001, # 服务端口, dev环境需要注意， 配置写的端口需要和转发到本地的端口保持一致（必要配置， 键不可修改）
    }
}

```

#### 使用示例：
```
from sparrow_django_common.utils.consul_service import ConsulService


consul = ConsulService()
# url返回 "host:prot"
url = consul.get_service_addr_consul(service_dependencies='SERVICE_DEPENDENCIES',
                                     service='SPARROW_XX_SERVICE')

                              
```


* * *

## 测试示例一（mock中间件中的requests）
```
from django.test import TestCase
from unittest import mock


# 第一步：写一个mocked_requests_get类， 用于mock 权限中间件中用的 request 方法
def mocked_requests_get(*args, **kwargs):

    class MockResponse:

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    # print(args[0])
    # import pdb; pdb.set_trace()
    if args[0].startswith('http://127.0.0.1:8001/api/sparrow_permission/i/isassigned/'):
        return MockResponse({"status": False}, 200)
    return MockResponse(None, 404)
    
    
# 第二步， 在测试方法中， 使用mock，把中间件的返回值修改

@mock.patch('sparrow_django_common.middleware.permission_middleware.requests.get', side_effect=mocked_requests_get)
  

```

## 测试示例二（mock中间件中的返回， 有权限返回 true， 没有权限返回flase）

```
from django.test import TestCase
from unittest import mock

# 在测试方法中， 使用mock，把中间件的返回值修改
@mock.patch('sparrow_django_common.middleware.permission_middleware.PermissionMiddleware.valid_permission', return_value=True)
  

```






