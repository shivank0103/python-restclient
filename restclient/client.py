from restclient.cas_service import CasRequest


class RestClient(CasRequest):
    """ Base class for initializing """

    def get_cas_token(self, service_name):
        pass

    def response(
            self, request_method: str, endpoint: str, headers=None, post_data=None, json_data=None, params=None
    ):
        """ Get API response """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if self.is_internal:
            auth_i_token = self.etcd.get_property_value('cas.internal.api.auth.secret')
            headers['Authorization-I'] = auth_i_token
        if request_method is None:
            raise Exception("Request method must be provided")
        if endpoint is None:
            raise Exception("Request endpoint must be provided")
        if self.service_name:
            self.base_url, authorization = self.get_service_base_url()
            headers['Authorization'] = 'Bearer ' + authorization
            headers['X-Service'] = self.app_name
        response, response_headers, status_code = self._get_api_response(
            self.base_url, request_method, endpoint, headers=headers, post_data=post_data, json_data=json_data, params=params
        )
        return response, response_headers, status_code
