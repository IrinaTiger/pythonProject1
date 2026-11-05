
import pytest
import requests

import psycopg2
from psycopg2.extras import RealDictCursor
from config import (
    BASE_URL_MARKETPLACE,
    HOST_SESSION,
    DATABASE_SESSION,
    USERNAME_SESSION,
    PASSWORD_SESSION,
    HOST_MARKETPLACE,
    DATABASE_MARKETPLACE,
    USERNAME_MARKETPLACE,
    PASSWORD_MARKETPLACE

    )


@pytest.fixture
def marketplace_db_session():
    """подключение к бд сессий маркетплейса"""
    connection=psycopg2.connect(
        host=HOST_SESSION,
        database=DATABASE_SESSION,
        user=USERNAME_SESSION,
        password=PASSWORD_SESSION
    )
    cursor=connection.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
    finally:
        connection.rollback()
        cursor.close()
        connection.close()


@pytest.fixture
def marketplace_db():
    connection=psycopg2.connect(
        host=HOST_MARKETPLACE,
        database=DATABASE_MARKETPLACE,
        user=USERNAME_MARKETPLACE,
        password=PASSWORD_MARKETPLACE
    )
    cursor=connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        connection.close()






#Получить неавторизированный x-key
@pytest.fixture
def session_non_authorized_x_key():
    session=requests.Session()
    url=f'{BASE_URL_MARKETPLACE}/buyer/v2/auth/login'
    res=session.post(url)
    assert res.status_code==400,f"Получен статус-код{res.status_code},надо 400"
    x_key=res.headers.get('x-key')
    assert x_key,f"Нет заголовка x-key"
    session.headers.update({"x-key": x_key})
    return session,x_key







@pytest.fixture
def get_headers():
    def _get_headers(x_key=None,jwt_token=None, buyer_id=None, language=None,x_city=None):

        headers = {}

        if jwt_token:
            headers["Token"] = jwt_token
        if buyer_id:
            headers["X-Buyer-Id"] = str(buyer_id)
        if language:
            headers["X-Language"] = language
        if x_key:
            headers["X-Key"]=x_key
        if x_city:
            headers["X-city"]=x_city

        return headers
    return _get_headers


