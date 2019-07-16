import logging
import consul
from django.core.exceptions import ImproperlyConfigured
from sparrow_django_common.utils.get_settings_value import GetSettingsValue

logger = logging.getLogger(__name__)


class ConsulService(object):
    """Consul服务， 接收服务名称， 返回域名"""
    def __init__(self):
        self.settings_value = GetSettingsValue()
        self.consul = self.settings_value.get_middleware_value('CONSUL')
        self.run_env = self.settings_value.get_settings_value('RUN_ENV')

    def get_service_addr_consul(self, service, schema=""):
        """
        获取服务的consul地址
        优先环境变量，如未配置环境变量，从consul中找服务， 如果是("dev", "unit")， 则使用127.0.0.1
        """
        port = self.settings_value.get_middleware_service_value(service, 'port')
        host = self.settings_value.get_middleware_service_value(service, 'host')
        service_name = self.settings_value.get_middleware_service_value(service, 'name')
        consul_client = consul.Consul(host=self.consul['host'],
                                      port=self.consul['port'],
                                      scheme="http")
        if self.run_env in ("dev", "unit"):
            logger.info("run_env=%s, 使用本地地址")
            address = '127.0.0.1'
            domain = "{schema}{address}:{port}".format(schema=schema, address=address, port=port)
            return domain
        if host and port:
            domain = "{schema}{address}:{port}".format(schema=schema, address=host, port=port)
            logger.info("domain={domain}".format(domain=domain))
            return domain
        try:
            port = consul_client.catalog.service(service_name)[1][0]['ServicePort']
            address = consul_client.catalog.service(service_name)[1][0]['ServiceAddress']
            domain = "{schema}{address}:{port}".format(schema=schema, address=address, port=port)
            return domain
        except Exception:
            raise ImproperlyConfigured("请检查settings.py 的consul配置是否正确")
