from clients.api_clients import ApiClient
from  config import (BASE_URL_MARKETPLACE)


class Authorization(ApiClient):
    def __init__(self):
        super().__init__(f"{BASE_URL_MARKETPLACE}/buyer/v1/")


    def auth_request(self,headers=None,json=None):
        endpoint="/auth/request"
        response=self.post(endpoint,headers=headers,json=json)
        return response

    def auth_confirm(self,headers=None,json=None):
        endpoint="/auth/confirm"
        response=self.post(endpoint,headers=headers,json=json)
        return response



