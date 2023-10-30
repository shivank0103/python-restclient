from restclient.base import BaseRestClient
from cashifycore.cache import CashifyCache


class CasRequest(BaseRestClient):
    """ Base class for CAS Authentication """

    GRANT_TYPE = 'implicit'
    SECURE_PREFIX = 'https://'
    NON_SECURE_PREFIX = 'http://'
    PRIVATE_SERVER_PREFIX = 'prv.'

    @CashifyCache('LOCAL').cache().cache('cashify_rest_client.oauth.token', 300, [])
    def _get_cas_response(self):
        base_url = self.etcd.get_property_value('cas.server.url')
        endpoint = 'v1/oauth/token'
        cas_data = {
            'grant_type': self.GRANT_TYPE,
            'client_id': self.app_name,
            'client_version': self.app_version
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response, response_headers, status_code = self._get_api_response(
            base_url=base_url, request_method='POST', endpoint=endpoint, headers=headers, post_data=cas_data
        )
        return response, response_headers, status_code

    def get_service_base_url(self):
        base_url = self.etcd.get_property_value('server.base.url')
        response, response_headers, status_code = self._get_cas_response()
        if response.get('isp') != 1:
            base_url = self.PRIVATE_SERVER_PREFIX + base_url

        for service in response['ser']:
            if service.get('key') == self.service_name:
                http_prefix = self.SECURE_PREFIX if service.get('is') else self.NON_SECURE_PREFIX
                base_url = http_prefix + service.get('si') + '.' + base_url
                return base_url, response.get('access_token')
        raise Exception("Invalid service key")
