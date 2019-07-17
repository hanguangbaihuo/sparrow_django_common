import requests
import logging
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from sparrow_django_common.utils.validation_data import VerificationConfiguration
from sparrow_django_common.utils.consul_service import ConsulService
from sparrow_django_common.utils.get_settings_value import GetSettingsValue
from sparrow_django_common.utils.normalize_url import NormalizeUrl
logger = logging.getLogger(__name__)


class PermissionMiddleware(object):
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
    def __init__(self):
        self.verification_configuration = VerificationConfiguration()
        self.verification_configuration.valid_permission_svc()
        self.settings_value = GetSettingsValue()
        self.url_join = NormalizeUrl()
        self.filter_path = self.settings_value.get_middleware_value(
            'PERMISSION_MIDDLEWARE', 'FILTER_PATH')
        self.service_name = self.settings_value.get_middleware_service_value(
            'PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE', 'name')
        self.permission_address = self.settings_value.get_middleware_service_value(
            'PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE', 'address')
        self.has_permission = True

    def process_request(self, request):
        # 验证中间件位置
        self.verification_configuration.verify_middleware_location(request)
        path = request.path
        method = request.method.upper()
        # 只校验有 不在 FILTER_PATH 中的url
        if path not in self.filter_path:
            if request.user.id:
                self.has_permission = self.valid_permission(path, method, request.user.id)
            if not self.has_permission:
                return JsonResponse({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)

    def valid_permission(self, path, method, user_id):
        """ 验证权限， 目前使用的是http的方式验证，后面可能要改成rpc的方式"""
        if all([path, method, user_id]):
            domain = ConsulService().get_service_addr_consul(service='PERMISSION_SERVICE')
            url = self.url_join.normalize_url(domain=domain, path=self.permission_address)
            post_data = {
                "path": path,
                "method": method,
                "user_id": user_id
            }
            response = requests.post(url, json=post_data)
            if response.status_code == 404:
                raise ImproperlyConfigured("请检查settings.py的permission_service配置的%s是否正确" % path)
            data = response.json()
            if response.status_code == 500:
                logger.error(data["message"])
                return True
            if 200 <= response.status_code < 300 and data['status']:
                return True
            return False
