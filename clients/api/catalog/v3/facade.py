
from clients.api.catalog.v3.models import CatalogLoginResponse
from clients.api.helpers.helpers import Checking,Models_Pydantic
import allure

import pytest
class CatalogFacade:
    def __init__(self,client):
        self.client=client

    def login_catalog_v3(self,phone,headers):
        #фасад успешной авторизации в каталоге
        body_catalog = {
            "phone": phone,
            "externalAuth": True
        }

        response=self.client.login_catalog(headers=headers,json=body_catalog)

        CatalogLoginResponse.model_validate(response.json())
        Models_Pydantic.validate_response(response.json(), CatalogLoginResponse)
        return response


    def login_not_user_catalog_v3(self,phone,headers):
        #фасад успешной авторизации в каталоге
        body_catalog = {
            "phone": phone,
            "externalAuth": True
        }

        response=self.client.login_catalog(headers=headers,json=body_catalog)

        return response

