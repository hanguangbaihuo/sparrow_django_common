# -*- coding: utf-8 -*-
from sparrow_django_common.utils.get_settings_value import GetSettingsValue

import importlib
import functools

JWT_AUTHENTICATION_MIDDLEWARE = 'JWT_AUTHENTICATION_MIDDLEWARE'
USER_CLASS_PATH = 'USER_CLASS_PATH'
ANONYMOUS_USER_CLASS_PATH = 'ANONYMOUS_USER_CLASS_PATH'


def get_settings_value():
    """Get the data in settings and add value validation"""
    settings_value = GetSettingsValue()
    user_class_path = settings_value.get_middleware_value(
        JWT_AUTHENTICATION_MIDDLEWARE, USER_CLASS_PATH)
    return user_class_path


@functools.lru_cache(maxsize=None)
def get_user_class():
    user_class_path = get_settings_value()
    module_path, cls_name = user_class_path.rsplit(".", 1)
    user_cls = getattr(importlib.import_module(module_path), cls_name)
    return user_cls

@functools.lru_cache(maxsize=None)
def get_anonymous_user_class():
    user_class_path = get_settings_value()
    module_path, cls_name = user_class_path.rsplit(".", 1)
    user_cls = getattr(importlib.import_module(module_path), cls_name)
    return user_cls