import unittest
import requests
from unittest import mock

from sparrow_django_common.middleware.permission_middleware import PermissionMiddleware


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:9999/api':
        return MockResponse({"status": "True", "message": "成功", }, 200)
    return MockResponse({"status": "False", "message": "失败"}, 200)


class TestStringMethods(unittest.TestCase):
    """测试permission_middleware"""

    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_middleware_value', return_value=[''])
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_middleware_service_value', return_value='api')
    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.verify_middleware_location', return_value='')
    @mock.patch('requests.get', side_effect=requests)
    @mock.patch('sparrow_django_common.middleware.permission_middleware.PermissionMiddleware.valid_permission', return_value=True)
    def test_process_request(self, valid_permission, request, verify_middleware_location, get_middleware_service_value, get_middleware_value, valid_permission_svc):
        self.assertEqual(PermissionMiddleware().process_request(request), None)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_settings_value', return_value='')
    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.valid_permission_svc',
                return_value='')
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_middleware_value',
                return_value=[''])
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_middleware_service_value',
                return_value='s')
    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.verify_middleware_location',
                return_value='')
    @mock.patch('sparrow_django_common.utils.consul_service.ConsulService.get_service_addr_consul', return_value='127.0.0.1:9999')
    def test_valid_permission(self, requests, get_service_addr_consul, verify_middleware_location,
                              get_middleware_service_value, get_middleware_value, valid_permission_svc, get_settings_value):
        self.assertEqual(PermissionMiddleware().valid_permission('path', 'method', 'user_id'), True)
