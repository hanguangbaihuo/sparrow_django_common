import unittest
from unittest import mock

from sparrow_django_common.utils.get_settings_value import GetSettingsValue


PERMISSION_MIDDLEWARE = {
    # 权限验证服务的配置
    "PERMISSION_SERVICE":{
        "name": "s-permission", #服务名称（k8s上的服务名）
        "host": "127.0.0.1", #IP
        "port": 8080, # 服务端口
        "address": "", # url
    },
    # consul服务的配置
    "CONSUL": {
        "host": "127.0.0.1", # ip
        "port": 9999, # 端口
    },
    "FILTER_PATH": [''], # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
    "METHOD_MAP": ('PUT', 'DELETE',) # 兼容阿里请求方式中间件配置， 保持默认的即可
}


class TestURLSplicing(unittest.TestCase):
    """测试url拼接"""

    def setUp(self):
        self.get_value = GetSettingsValue()
        self.get_value.get_settings_value = mock.Mock(return_value=PERMISSION_MIDDLEWARE)
        self.get_value.get_middleware_value = mock.Mock(return_value=PERMISSION_MIDDLEWARE['PERMISSION_SERVICE'])

    def test_get_middleware_value(self):
        service_value = self.get_value.get_settings_value('PERMISSION_MIDDLEWARE')
        value = service_value.get('PERMISSION_SERVICE', None)
        self.assertEqual(value, PERMISSION_MIDDLEWARE['PERMISSION_SERVICE'])

    def test_get_middleware_service_value(self):
        middleware_value = self.get_value.get_middleware_value()
        value = middleware_value.get('name', None)
        self.assertEqual(value, PERMISSION_MIDDLEWARE['PERMISSION_SERVICE']['name'])


if __name__ == '__main__':
    unittest.main()