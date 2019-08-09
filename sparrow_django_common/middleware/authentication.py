# -*- coding: utf-8 -*-
from rest_framework.authentication import get_authorization_header
from sparrow_django_common.common.utils import get_user_class
from sparrow_django_common.common.decode_jwt import DecodeJwt
import logging

logger = logging.getLogger(__name__)


class SparrowAuthentication(object):

    USER_CLASS = get_user_class()

    def authenticate(self, request):
        '''
        HTTP_AUTHORIZATION': 'Token eyJhbGciOiJIU.eyJpc3MiOiWTy.z0HODSJhWtFzX'
        try to create user Model from UserModel
            if suc : return user
            if falied: return None
        '''
        try:
            payload = request.META['payload']
            user_id = request.META['REMOTE_USER']
            user = self.get_user(user_id, payload)
        except Exception as ex:
            logger.error(ex)
            return None
        return (user, payload)

    def get_user(self, user_id, payload):
        user = self.USER_CLASS(user_id=user_id)
        user.payload = payload
        return user

    def authenticate_header(self, request):
        return "Token"