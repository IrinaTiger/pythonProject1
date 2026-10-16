from clients.api.v1.authorization.authorization_client import Authorization
import json
import allure
from clients.api.catalog.v3.buyer_client import Authorization_Catalog
from curlify import to_curl
from clients.api.catalog.v3.models import Authorization_catalog
from clients.api.helpers.helpers import Checking
from clients.api.catalog.facade import CatalogFacade
from clients.api.v1.authorization.Facades.FacadesV1.FacadeAuthorization import FacadeAuthorization
import pytest

@allure.title("Авторизация пользователя")
def test_auth_request(session_non_authorized_x_key,get_headers,delete_user_by_phone_from_db_session):
    phone = "79991234515"
    delete_user_by_phone_from_db_session(phone)
    _,x_key=session_non_authorized_x_key
    headers=get_headers(
        x_key=x_key
    )

    body={
     "phone": phone,
     "captcha": ""
    }
    clients=Authorization()
    response=clients.auth_request(json=body,headers=headers)
    print(response.json())
    assert response.status_code==200


#тест - идем в каталог- смотрим, что по телефону есть пользак
#идем в маркет - вход


@pytest.mark.parametrize("phone",[
    "79154004274"
])
def test_authontification(catalog_headers_simple,
                          login_catalog,
                          delete_user_by_phone_from_db_session,
                          phone,
                          auth_request_marketplace):

    #запрос в catalog-buyer найден(200)- авторизация в маркет

    #запрос в католог
    login_catalog.login_catalog_v3(phone=phone, headers=catalog_headers_simple)

    #чистка бд маркета
    delete_user_by_phone_from_db_session(phone)

    response=auth_request_marketplace.auth_request(phone=phone)





