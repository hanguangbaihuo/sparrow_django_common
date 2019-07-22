import unittest
from unittest import mock

from sparrow_django_common.common.user import User


AUTH = b'Token eyJhUzI1NiIs'
USER_ID = '3aa60781234547a5b94a095588999999'
PAYLOAD = {'uid': '3aa60781234547a5b94a095588999999', 'app_id': 'app_0000',
           'exp': 0000, 'iat': 1111, 'iss': 'd'}
USER = User(user_id=USER_ID)


class TestJWT(unittest.TestCase):

    @mock.patch('sparrow_django_common.middleware.authentication.JWTAuthentication.get_user', return_value=USER_ID)
    @mock.patch('sparrow_django_common.middleware.authentication.JWTAuthentication.USER_CLASS', return_value=USER)
    @mock.patch('rest_framework.authentication.get_authorization_header', return_value=AUTH)
    @mock.patch('sparrow_django_common.common.utils.get_settings_value', return_value='sparrow_django_common.common.'
                                                                                      'user.User')
    @mock.patch('sparrow_django_common.common.utils.get_user_class', return_value=USER)
    @mock.patch('django.conf.settings', return_value='')
    @mock.patch('sparrow_django_common.common.decode_jwt.DecodeJwt.decode_jwt', return_value=PAYLOAD)
    @mock.patch('sparrow_django_common.utils.get_settings_value.GetSettingsValue.get_middleware_value',
                return_value='mock_value')
    def test_jwt(self, get_middleware_value, DecodeJwt, settings, get_user_class, get_settings_value,
                 get_authorization_header, USER_CLASS, get_user):
        from sparrow_django_common.middleware.authentication import JWTAuthentication
        self.assertEqual(JWTAuthentication().authenticate('request'), (USER_ID, PAYLOAD))


if __name__ == '__main__':
    unittest.main()
