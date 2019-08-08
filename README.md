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
kubectl get pods -n default | grep sparrow-permissioin | awk '{print "kubectl port-forward "$1 " 8001:8001 -n default"}' |sh
```


#### 二、配置PERMISSION_MIDDLEWARE需要的参数
> 将以下参数添加到settings.py 

```
PERMISSION_MIDDLEWARE = {
    # 权限验证服务的配置
    "PERMISSION_SERVICE":{
        "name": "sparrow-permission-svc", #服务名称（k8s上的服务名）
        "host": "127.0.0.1", #IP
        "port": 8001, # 服务端口, dev环境需要注意， 配置写的端口需要和转发到本地的端口保持一致
        "address": "api/sparrow_permission/i/isassigned/", # url
    },
    "FILTER_PATH" : [''], # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
}


# 权限中间件需要到consul中去发现权限服务的地址， 所以需要配置consul服务的地址
CONSUL_CLIENT_ADDR = {
    "host": "127.0.0.1",
    "port": 8500
}
```

> 描述
 - PERMISSION_MIDDLEWARE : 中间件配置
   -  PERMISSION_SERVICE ：权限验证配置
        - name : 服务名称（k8s上的服务名， 必要配置）
        - host : 主机地址(非必要配置，如果配置了，则走配置中的host， 不配置从consul中查找服务)
        - port : 服务端口（必要配置）
        - address : 权限服务的path（必要配置）
   -  FILTER_PATH : [] ,使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中（非必要配置）
   
   
-  CONSUL_CLIENT_ADDR： consul配置
   - host : 主机地址（必要配置）
   - port : 服务端口（必要配置）
   
#### 注册 PERMISSION_MIDDLEWARE 
> 注册中间件
```
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        'sparrow_django_common.middleware.permission_middleware.PermissionMiddleware',    #权限中间件
    )
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

## JWT_AUTHENTICATION_MIDDLEWARE
> 描述：
```buildoutcfg

```

#### 配置 JWT_AUTHENTICATION_MIDDLEWARE 中间件需要的参数
> 将以下参数添加到settings.py
```
JWT_AUTHENTICATION_MIDDLEWARE = {
    "JWT_SECRET": "问 tianyi",
    "USER_CLASS_PATH": "sparrow_django_common.common.user.User", 
}
``` 
> 参数说明： USER_CLASS_PATH： 路径中的User为中间件的User模版， 可以根据自己的需求重新创建User， 并将自己的User路径按照模版格式放到：USER_CLASS_PATH下 

#### 注册 JWT_AUTHENTICATION_MIDDLEWARE

> 注册中间件
```
REST_FRAMEWORK{
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'sparrow_django_common.middleware.authentication.JWTAuthentication',      
    }
```















