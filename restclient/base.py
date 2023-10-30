import requests
from cashifyetcd import CashifyETCD


class SingleTonETCD(object):
    _instance = None
    _etcd = None

    def __new__(cls, etcd_host: str, etcd_port: int, etcd_protocol: str, service_name: str, service_version: str):
        if cls._instance is None:
            cls._instance = super(SingleTonETCD, cls).__new__(cls)
            cls._etcd = CashifyETCD(
                host=etcd_host, protocol=etcd_protocol, port=etcd_port,
                service_version=service_version, service_name=service_name
            )
        return cls._etcd


class BaseRestClient(object):
    """ Base class for initializing """

    TIMEOUT = 30
    REQUEST_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    base_url = None
    app_name = None
    app_version = None
    service_name = None
    service_version = None
    is_internal = False
    etcd_host = None
    etcd_port = None
    etcd_protocol = None
    etcd = None

    def __init__(
            self, app_name: str = None, app_version: str = 'v1', base_url: str = None,
            service_name: str = None, service_version: str = 'v1', is_internal: bool = False,
            etcd_host: str = None, etcd_port: int = None, etcd_protocol: str = None
    ):

        """ init rest client """

        self.base_url = base_url
        self.app_name = app_name
        self.service_name = service_name
        self.app_version = app_version
        self.service_version = service_version
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.etcd_protocol = etcd_protocol
        self.is_internal = is_internal
        self.etcd = SingleTonETCD(
            etcd_host=etcd_host, etcd_port=etcd_port, etcd_protocol=etcd_protocol,
            service_name=app_name, service_version=app_version
        )

    def _get_api_response(
            self, base_url, request_method, endpoint, headers=None, post_data=None, json_data=None, params=None, timeout=None
    ):
        """ Get API response """
        if not request_method or request_method not in self.REQUEST_METHODS:
            raise Exception("Provide correct request method")

        url = "%s/%s" % (base_url, endpoint)

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if timeout is None:
            timeout = self.TIMEOUT
        response = requests.request(
            method=request_method, url=url, data=post_data, json=json_data, params=params, headers=headers, timeout=timeout
        )
        if isinstance(response.content, dict):
            return response.json(), response.headers, response.status_code
        if isinstance(response.content, (bytes, bytearray)):
            try:
                return response.json(), response.headers, response.status_code
            except Exception as e:
                print(e)
                return response.text, response.headers, response.status_code
        return response.content, response.headers, response.status_code
