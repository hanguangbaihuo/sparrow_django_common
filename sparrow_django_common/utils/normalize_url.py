from urllib.parse import urljoin


class NormalizeUrl(object):
    """url拼接， 使用场景：consul返回服务的域名，将域名和path拼接"""

    def normalizeurl(self, domain, path, scheme='http'):
        """url 拼接"""
        service_addr = "".join([scheme, '://', domain])
        url = urljoin(service_addr, path)
        return url




