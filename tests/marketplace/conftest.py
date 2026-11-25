import pytest
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

from clients.api.helpers.helpers_db import SessionDbHelper
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


# ---------- Подключения к БД маркетплейса ----------

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


# ---------- Сессия ----------

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


# ---------- Конфиг маркетплейса (public.config) ----------

@pytest.fixture
def check_config_ecom(marketplace_db):
    original = {}

    def _set_config_ecom(alias, value):
        marketplace_db.execute("select value from public.config where alias=%s", (alias,))
        row = marketplace_db.fetchone()
        assert row is not None, f"Запрос по {alias} не найден"
        original.setdefault(alias, row[0])

        marketplace_db.execute("UPDATE public.config SET value=%s where alias=%s",
                               (str(value), alias))
        marketplace_db.connection.commit()
        return value

    yield _set_config_ecom

    for alias, value in original.items():
        marketplace_db.execute("UPDATE public.config SET value=%s where alias=%s",
                               (value, alias))
    marketplace_db.connection.commit()


# ---------- БД сессий: очистка и проверки по телефону ----------

@pytest.fixture
def delete_user_by_phone_from_db_session(marketplace_db_session,phone):

        marketplace_db_session.execute("DELETE  from buyer.log_confirm "
                                  "where phone=%s",
                                       (phone,))
        marketplace_db_session.connection.commit()

        marketplace_db_session.execute("SELECT *  from buyer.log_confirm "
                                  "where phone=%s",
                                       (phone,))

        assert marketplace_db_session.fetchall()==[]

        marketplace_db_session.execute("DELETE  from buyer.confirm_request "
                                  "where phone=%s",
                                  (phone,))
        marketplace_db_session.connection.commit()

        marketplace_db_session.execute("SELECT *  from buyer.confirm_request "
                                       "where phone=%s",
                                       (phone,))

        assert marketplace_db_session.fetchall() == []
        return phone


@pytest.fixture
def db_session_log_confirm_by_phone(marketplace_db_session):
    def _log_confirm_by_phone(phone,expected_data):
        return SessionDbHelper.checking_session_log_confirm_by_phone(marketplace_db_session,phone,expected_data)

    return _log_confirm_by_phone

@pytest.fixture
def db_session_confirm_request_by_phone(marketplace_db_session):
    def _confirm_request_by_phone(phone,expected_data):
        return SessionDbHelper.checking_session_confirm_request_by_phone(marketplace_db_session,phone,expected_data)

    return _confirm_request_by_phone
