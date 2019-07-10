import logging
import os
import consul
import jwt
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class PermissionValidError(Exception):
    pass


# tina姐权限模块的服务名称
PERMISSION_SVC = {
    "pro": "pro-sparrow-permission-svc",
    "dev": "sparrow-permission-svc",
    "test": "sparrow-permission-svc",
    "unit": "",
}


class PermissionMiddleware(object):
    """
    权限中间件
    使用方法：
        1.导入此文件到项目中
        2.将此中间件放在 AuthenticationMiddleware 之后
    工作原理：
                                (url + method + user_id)
                                        |                       / 有权限则允许通过
    request -> PermissionMiddleware ---https---> tina姐写的权限模块
                                                                \ 无权限则返回HTTP 403错误

    """

    def process_request(self, request):
        # 验证中间件放的位置
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "PermissionMiddleware"
                " 应该放置在"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " 后面")
        has_permission = True
        path = request.path
        method = request.method.upper()
        # 只校验有 "/api/" 的url
        if "/api/" in path:
            if request.user.id:
                has_permission = self.valid_permission(path, method, request.user.id)
            else:
                user_id = self.get_user_id_by_token(request)
                if user_id:
                    has_permission = self.valid_permission(path, method, user_id)
            if not has_permission:
                return JsonResponse({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)

    def get_user_id_by_token(self, request):
        """校验token"""
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        try:
            token = auth[1]
            payload = self.decode_jwt(token)
            user_id = payload["uid"]
        except Exception as ex:
            return None
        return user_id

    def valid_permission(self, path, method, user_id):
        """ 验证权限， 目前使用的是http的方式验证，后续要改成rpc的方式"""
        if all([path, method, user_id]):
            # service_name = PERMISSION_SVC[settings.RUN_ENV]
            service_name = get_value("PERMISSION_SVC")
            service_addr = get_service_addr(service_name)
            url = "".join(["http://", service_addr, "/api/sparrow_permission/user/isassigned/"])
            post_data = {
                "path": path,
                "method": method,
                "user_id": user_id
            }
            # 需要tina把 token验证去掉， 因为已经传了 user_id, 如果用户是用的
            headers = {
                "AUTHORIZATION": "Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI5ZGFhMDc5NjhmOTU0OGE1OTBjYzhiNzM2M2Y3MzlkMCIsImFwcF9pZCI6ImFwcF8xNTIxMDEwNzg4IiwiZXhwIjoxNTYyNzMyMDA3LCJpYXQiOjE1NjI2NDU2MDcsImlzcyI6ImJhY2tlbmQifQ.Y0bS9w0Jm6o6GOQYpZFjU5Gxup5pnCKh75w1mpr7qvw"
            }
            response = requests.post(url, json=post_data, headers=headers)
            data = response.json()
            if response.status_code != status.HTTP_200_OK:
                logger.error(data["message"])
                raise PermissionValidError(data["message"])
            if data["status"] and data["message"] in ["1", 1]:
                return True
            return False

    def decode_jwt(self, token):
        """token 解码"""
        secret = settings.JWT_SECRET
        try:
            payload = jwt.decode(token, secret, algorithms='HS256')
        except Exception as ex:
            raise ex
        return payload


def get_value(name):
    """ 获取权限的环境变量（为支持开发环境的权限验证， 获取开发环境的PERMISSION_SVC，并将测试环境的服务转发到本地 ）"""
    value = os.environ.get(name, PERMISSION_SVC.get(settings.RUN_ENV, None))
    if value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def get_setting_value(name):
    value = os.environ.get(name, getattr(settings, name, None))
    if value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def get_service_addr(service_name, schema=""):
    """从consul服务中读到需要需要访问的服务的域名"""
    # import pdb; pdb.set_trace()
    # 2019-06-25 紧急情况，跳过consul
    if ":" in service_name:
        domain = "{schema}{address}".format(
            schema=schema, address=service_name)
        logger.info("domain={domain}".format(domain=domain))
        return domain

    run_env = get_setting_value("RUN_ENV")
    consul_client_addr = get_setting_value("CONSUL_CLIENT_ADDR")

    consul_client = consul.Consul(
        host=consul_client_addr['host'],
        port=consul_client_addr['port'],
        scheme="http"
    )
    port = ""
    address = ""
    try:
        port = consul_client.catalog.service(service_name)[1][0]['ServicePort']
        address = consul_client.catalog.service(service_name)[1][0]['ServiceAddress']
    except Exception as ex:
        logger.error(ex)
        domain = ""
    # services = consul_client.agent.services()
    # if run_env in ("dev", "unit"):
    #     logger.info("run_env=%s, 使用本地地址")
    #     address = "127.0.0.1"
    #     port = "8001"
    if run_env in ("dev", "unit"):
        logger.info("run_env=%s, 使用本地地址")
        address = "127.0.0.1"
        port = "8001"
    domain = "{schema}{address}:{port}".format(schema=schema, address=address, port=port)
    logger.info("domain={domain}".format(domain=domain))
    return domain
