import requests
import logging

from django.core.exceptions import ImproperlyConfigured

from rest_framework import permissions

from sparrow_django_common.utils.validation_data import VerificationConfiguration
from sparrow_django_common.utils.consul_service import ConsulService
from sparrow_django_common.utils.get_settings_value import GetSettingsValue
from sparrow_django_common.utils.normalize_url import NormalizeUrl
logger = logging.getLogger(__name__)


class PermissionMiddleware(permissions.BasePermission):
    """
    权限中间件
    使用方法：
        1.导入此文件到项目中
        2.将此中间件放在 AuthenticationMiddleware 之后
    工作原理：
                                (url + method + user_id)
                                        |               / 有权限则允许通过
    request -> PermissionMiddleware ---https---> 权限模块
                                                        \ 无权限则返回HTTP 403错误

    """
    VERIFICATION_CONGIGURATION = VerificationConfiguration()
    VERIFICATION_CONGIGURATION.valid_permission_svc()
    SETTINGS_VALUE = GetSettingsValue()
    URL_JOIN = NormalizeUrl()
    FILTER_PATH = SETTINGS_VALUE.get_middleware_value(
        'PERMISSION_MIDDLEWARE', 'FILTER_PATH')
    SERVICE_NAME = SETTINGS_VALUE.get_middleware_service_value(
        'PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE', 'name')
    PERMISSION_ADDRESS = SETTINGS_VALUE.get_middleware_service_value(
        'PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE', 'address')
    HAS_PERMISSION = False

    def has_permission(self, request, view):
        # 验证中间件位置
        path = request.path
        method = request.method.upper()
        url = request.META.get('HTTP_REFERER', None)
        # 只校验有 不在 FILTER_PATH 中的url
        if path not in self.FILTER_PATH:
            if request.user and request.user.is_authenticated():
                self.HAS_PERMISSION = self.valid_permission(path, method, request.user.id)
            if self.HAS_PERMISSION:
                return True
            return False
        elif url is not None:
            if url.__contains__("login"):
                return True
            return False
        return True

    def valid_permission(self, path, method, user_id):
        """ 验证权限， 目前使用的是http的方式验证，后面可能要改成rpc的方式"""
        if all([path, method, user_id]):
            domain = ConsulService().get_service_addr_consul(service='PERMISSION_SERVICE')
            url = self.URL_JOIN.normalize_url(
                domain=domain, path=self.PERMISSION_ADDRESS)
            post_data = {
                "path": path,
                "method": method,
                "user_id": user_id
            }
            try:
                response = requests.post(url, json=post_data)
            except Exception as ex:
                logger.error(ex)
                return True
            if response.status_code == 404:
                raise ImproperlyConfigured(
                    "请检查settings.py的permission_service配置的%s是否正确" % path)
            data = response.json()
            if response.status_code == 500:
                logger.error(data["message"])
                return True
            if 200 <= response.status_code < 300 and data['status']:
                return True
            return False
