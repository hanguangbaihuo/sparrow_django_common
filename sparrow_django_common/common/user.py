# -*- coding: utf-8 -*-


class User(object):
    '''自定义的 User 对象'''
    def __init__(self, user_id, ):
        self._id = user_id
        self._is_authenticated = True

    def is_authenticated(self):
        return True

    @property
    def id(self):
        return self._id

    def username():
        doc = "The username property."
        def fget(self):
            return self._username
        def fset(self, value):
            self._username = value
        def fdel(self):
            del self._username
        return locals()
    username = property(**username())

    def payload():
        doc = "The payload property."
        def fget(self):
            return self._payload
        def fset(self, value):
            self._payload = value
        def fdel(self):
            del self._payload
        return locals()
    payload = property(**payload())

    @property
    def member_xx(self):
        # TODO
        return {
            "name": "会员",
            "account_id": "000000",
            "number": "180000423",
            "birthday": "1990-09-01",
            "sex": "F",
            "status": "OPEN",
            "level": "MEMBER_L2",
        }


class AnonymousUser(object):
    def __init__(self,user_id):
        self._id = user_id

    @property
    def id(self):
        return self._id

    def payload():
        doc = "The payload property."
        def fget(self):
            return self._payload
        def fset(self, value):
            self._payload = value
        def fdel(self):
            del self._payload
        return locals()
    payload = property(**payload())

    @property
    def is_authenticated(self):
        return False

    
