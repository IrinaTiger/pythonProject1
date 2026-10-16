
import clients.headers_builder
from clients.api.catalog.facade import CatalogFacade
from clients.api.v1.authorization.Facades.FacadesV1.FacadeAuthorization import FacadeAuthorization

import pytest
import requests

import psycopg2
from psycopg2.extras import RealDictCursor
import allure
from clients.headers_builder import Headers_marketplace
import config
from config import (
    BASE_URL_MARKETPLACE,
    HOST,
    DATABASE,
    USERNAME,
    PASSWORD,
    HOST_SESSION,
    DATABASE_SESSION,
    USERNAME_SESSION,
    PASSWORD_SESSION,
    BASE_URL_NOTIFICATION_CENTER,
    JWT_TOKEN_BASE_BASE_URL,
    HOST_SESSION_NOTIFICATION_CENTER,
    DATABASE_SESSION_NOTIFICATION_CENTER,
    USERNAME_NOTIFICATION_CENTER,
    PASSWORD_NOTIFICATION_CENTER,
    HOST_JWT_CATALOG,
    SECRET_JWT_CATALOG,
    ISSUER_JWT_CATALOG,
    SUBJECT_JWT_CATALOG,
    EXPIRE_JWT_CATALOG
    )

from curlify import to_curl
from clients.api.v1.authorization.authorization_client import Authorization

#Получить неавторизированный x-key 
@pytest.fixture
def session_non_authorized_x_key():
    session=requests.Session()
    url=f'{BASE_URL_MARKETPLACE}/buyer/v2/auth/login'
    res=requests.post(url)
    x_key=res.headers.get('x-key')
    session.headers.update({"x-key": x_key})
    return session,x_key

#Подключится к бд сессий маркета
@pytest.fixture
def db_session_connection():
    print(DATABASE_SESSION)
    connection=psycopg2.connect(
    host=HOST_SESSION,
    database =DATABASE_SESSION,
    user= USERNAME_SESSION,
    password = PASSWORD_SESSION
    )
    connection.autocommit=False
    try:
        yield connection
    finally:
        connection.rollback()
        connection.close()

@pytest.fixture
def cursor_db_session(db_session_connection):
    with db_session_connection.cursor(cursor_factory=RealDictCursor) as cursor:
        yield cursor



@allure.title('Генерация токена JWT для Notification Centre')
@pytest.fixture
def generate_jwt_token_notification_center():

    params={
        "host":"notification-center-stage.ecom.fix-price.ru",
        "secret":"xieT3iesei0ahdoh2ohyfhTF89KhdgQ5",
        "issuer":"Notification Center",
        "subject":"NOTIFICATION",
        "expire":"36000"
    }

    get_jwt=requests.get(JWT_TOKEN_BASE_BASE_URL,params=params)
    assert get_jwt.status_code==200,f"JWT токен не получен, код {get_jwt.status_code}"
    return get_jwt.json().get ("token")


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
def db_notification_centre():
    connection=psycopg2.connect(
        host=HOST_SESSION_NOTIFICATION_CENTER,
        database=DATABASE_SESSION_NOTIFICATION_CENTER,
        user=USERNAME_NOTIFICATION_CENTER,
        password=PASSWORD_NOTIFICATION_CENTER
    )
    cursor=connection.cursor()

    yield cursor

    cursor.close()
    connection.close()
@pytest.fixture
def get_headers():
    def _get_headers(x_key=None,jwt_token=None, buyer_id=None, language=None):

        headers = {}

        if jwt_token:
            headers["Token"] = jwt_token
        if buyer_id:
            headers["X-Buyer-Id"] = str(buyer_id)
        if language:
            headers["X-Language"] = language
        if x_key:
            headers["X-Key"]=x_key

        return headers
    return _get_headers

@pytest.fixture
def login_catalog(client_catalog_create):
    return CatalogFacade(client_catalog_create)


@pytest.fixture
def client_marketplace_Authorization():
    client=Authorization()
    return client

@pytest.fixture
def auth_request_marketplace(client_marketplace_Authorization,session_non_authorized_x_key,get_headers):
    _, x_key = session_non_authorized_x_key
    headers = get_headers(x_key=x_key)
    return FacadeAuthorization(client_marketplace_Authorization,headers)