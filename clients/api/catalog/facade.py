from clients.api.catalog.v3.models import Authorization_catalog
from clients.api.catalog.v3.models import Authorization_catalog
from clients.api.helpers.helpers import Checking,Models_Pydantic
import allure

import pytest
class CatalogFacade:
    def __init__(self,client):
        self.client=client

    def login_catalog_v3(self,phone,headers,expected_status=200):
        #фасад успешной авторизации в каталоге
        body_catalog = {
            "phone": phone,
            "externalAuth": True
        }

        response=self.client.login_catalog(headers=headers,json=body_catalog)

        Authorization_catalog.model_validate(response.json())
        Models_Pydantic.validate_response(response.json(), Authorization_catalog)
        return response