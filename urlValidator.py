from urllib.parse import urlparse, urlsplit
from flask import request

def url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    if not url:
        return False
    
    url_info = urlsplit(url)
    scheme = url_info.scheme
    netloc = url_info.netloc
    
    allowed_schemes = {'https'} if require_https else {'http', 'https'}
    
    if scheme not in allowed_schemes:
        return False
    
    if allowed_hosts is None:
        return True
    
    if isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}

    return netloc in allowed_hosts or (
        netloc.replace('\\', '/') in allowed_hosts
    )