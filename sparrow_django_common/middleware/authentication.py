# -*- coding: utf-8 -*-
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from sparrow_django_common.common.utils import get_user_class
from sparrow_django_common.common.decode_jwt import DecodeJwt
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(object):

    USER_CLASS = get_user_class()

    def authenticate(self, request):
        '''
        HTTP_AUTHORIZATION': 'Token eyJhbGciOiJIU.eyJpc3MiOiWTy.z0HODSJhWtFzX'
        try to create user Model from UserModel
            if suc : return user
            if falied: return None
        '''
        auth = get_authorization_header(request).split()
        # 如果未认证, 返回空
        if not auth or auth[0].lower() != b'token':
            return (None, None)
        try:
            token = auth[1]
            payload = DecodeJwt().decode_jwt(token)
            user_id = payload["uid"]
            user = self.get_user(user_id, payload)
        except Exception as ex:
            logger.error(ex)
            msg = 'Invalid token. auth={0}, error={1}'.format(auth, ex)
            raise exceptions.AuthenticationFailed(msg)
        return (user, payload)

    def get_user(self, user_id, payload):
        user = self.USER_CLASS(user_id=user_id)
        user.payload = payload
        return user

    def authenticate_header(self):
        return "Token"
