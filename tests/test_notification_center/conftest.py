
import pytest
import requests
import psycopg2
import allure
from config import (
    BASE_URL_NOTIFICATION_CENTER,
    JWT_TOKEN_BASE_BASE_URL,
    HOST_SESSION_NOTIFICATION_CENTER,
    DATABASE_SESSION_NOTIFICATION_CENTER,
    USERNAME_NOTIFICATION_CENTER,
    PASSWORD_NOTIFICATION_CENTER,
    SECRET_HOST_JWT_NOTIFICATION,
    HOST_JWT_NOTIFICATION
    )
@allure.title('Генерация токена JWT для Notification Centre')
@pytest.fixture
def generate_jwt_token_notification_center():

    params={
        "host":HOST_JWT_NOTIFICATION,
        "secret":SECRET_HOST_JWT_NOTIFICATION,
        "issuer":"Notification Center",
        "subject":"NOTIFICATION",
        "expire":"36000"
    }

    get_jwt=requests.get(JWT_TOKEN_BASE_BASE_URL,params=params)
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