
from clients.api.helpers.helpers import Checking
from clients.headers_builder import Headers_catalog
from clients.api.catalog.v3.client import Authorization_Catalog


from clients.api.catalog.v3.facade import CatalogFacade
import pytest
import requests

from config import (
    JWT_TOKEN_BASE_BASE_URL,
    HOST_JWT_CATALOG,
    SECRET_JWT_CATALOG,
    ISSUER_JWT_CATALOG,
    SUBJECT_JWT_CATALOG,
    EXPIRE_JWT_CATALOG
    )
from curlify import to_curl

@pytest.fixture
def catalog_headers_simple(generate_jwt_token_catalog,country):
    headers = (
        Headers_catalog()
        .with_x_api_key(generate_jwt_token_catalog)
        .with_cns_agent("Web CNS Fix-Price")
        .with_x_country(country)
        .build()
    )
    return headers

@pytest.fixture
def client_catalog_create():
    clients=Authorization_Catalog()
    return clients


@pytest.fixture
def generate_jwt_token_catalog():
    params={
        'host':HOST_JWT_CATALOG,
        'secret':SECRET_JWT_CATALOG,
        'issuer':ISSUER_JWT_CATALOG,
        'subject':SUBJECT_JWT_CATALOG,
        'expire':EXPIRE_JWT_CATALOG

        }
    response=requests.get(url=JWT_TOKEN_BASE_BASE_URL,params=params)
    print(to_curl(response.request))
    assert  response.status_code==200,f"JWT токен не получен, ответ: {response.json()}"
    return response.json().get("token")


@pytest.fixture
def catalog_facade(client_catalog_create):
    return CatalogFacade(client_catalog_create)





@pytest.fixture
def user_exist_in_catalog(catalog_headers_simple,
                             catalog_facade,
                             phone):
    response_catalog = catalog_facade.login_catalog_v3(phone=phone, headers=catalog_headers_simple)
    Checking.assert_status_code(response_catalog, 200)


@pytest.fixture
def user_not_exist_in_catalog(catalog_headers_simple,
                             catalog_facade,
                             phone):
    response_catalog=catalog_facade.login_not_user_catalog_v3(phone=phone,headers=catalog_headers_simple)
    Checking.assert_status_code(response_catalog, 400)
    assert  response_catalog.json().get("message")=="Пользователь не найден",f"Телефон {phone} уже зарегистрирован"




