import os
from dotenv import load_dotenv
load_dotenv()
import pytest
import requests

import psycopg2
from psycopg2.extras import RealDictCursor
import allure


BASE_URL=os.getenv("BASE_URL")
HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")
USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")
HOST_SESSION=os.getenv("HOST_SESSION")
DATABASE_SESSION=os.getenv("DATABASE_SESSION")
USERNAME_SESSION=os.getenv("USERNAME_SESSION")
PASSWORD_SESSION=os.getenv("PASSWORD_SESSION")
BASE_URL_NOTIF_CENTRE=os.getenv("BASE_URL_NOTIFICATION_CENTER")
JWT_TOKEN_BASE_BASE_URL_NOTIFICATION_CENTER=os.getenv("JWT_TOKEN_BASE_BASE_URL_NOTIFICATION_CENTER")
HOST_SESSION_NOTIFICATION_CENTER=os.getenv("HOST_SESSION_NOTIFICATION_CENTER")
DATABASE_SESSION_NOTIFICATION_CENTER=os.getenv("DATABASE_SESSION_NOTIFICATION_CENTER")
USERNAME_NOTIFICATION_CENTER=os.getenv("USERNAME_NOTIFICATION_CENTER")
PASSWORD_NOTIFICATION_CENTER=os.getenv("PASSWORD_NOTIFICATION_CENTER")



#Получить неавторизированный x-key 
@pytest.fixture
def session_non_authorized_x_key():
    session=requests.Session()
    url=f'{BASE_URL}/buyer/v2/auth/login'
    res=requests.post(url)
    x_key=res.headers.get('x-key')
    session.headers.update({"x-key": x_key})
    return session,x_key

#Подключится к бд сессий маркета
@pytest.fixture
def db_session_connection():
    connection=psycopg2.connect(
    host=os.getenv("HOST_SESSION"),
    database = os.getenv("DATABASE_SESSION"),
    user= os.getenv("USERNAME_SESSION"),
    password = os.getenv("PASSWORD_SESSION")

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
def generate_jwt_token():

    params={
        "host":"notification-center-stage.ecom.fix-price.ru",
        "secret":"xieT3iesei0ahdoh2ohyfhTF89KhdgQ5",
        "issuer":"Notification Center",
        "subject":"NOTIFICATION",
        "expire":"36000"
    }

    get_jwt=requests.get(JWT_TOKEN_BASE_BASE_URL_NOTIFICATION_CENTER,params=params)
    assert get_jwt.status_code==200,f"JWT токен не получен, код {get_jwt.status_code}"
    return get_jwt.json().get ("token")

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
    def _get_headers(jwt_token=None, buyer_id=None, language=None):

        headers = {}

        if jwt_token:
            headers["Token"] = jwt_token
        if buyer_id:
            headers["X-Buyer-Id"] = str(buyer_id)
        if language:
            headers["X-Language"] = language

        return headers
    return _get_headers

