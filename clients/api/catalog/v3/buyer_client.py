from clients.api_clients import ApiClient
from config import BASE_URL_CATALOG

class Authorization_Catalog(ApiClient):
    def __init__(self):
        super().__init__(f"{BASE_URL_CATALOG}/v3/buyer/")

    def login_catalog(self,headers=None,json=None,body=None):
        endpoint='/login'
        response=self.post(endpoint,headers=headers,json=json)
        return response