import psycopg2
import pytest
from clients.headers_builder import Headers_catalog
from clients.api.catalog.v3.buyer_client import Authorization_Catalog
from config import (HOST,
                DATABASE,
                USERNAME,
                PASSWORD,
                HOST_SESSION,
                DATABASE_SESSION,
                USERNAME_SESSION,
                PASSWORD_SESSION,
                BASE_URL_CATALOG)


@pytest.fixture
def marketplace_db_session():
    """подключение к бд сессий маркетплейса"""
    connection=psycopg2.connect(
        host=HOST_SESSION,
        database=DATABASE_SESSION,
        user=USERNAME_SESSION,
        password=PASSWORD_SESSION
    )
    cursor=connection.cursor()
    try:
        yield cursor
    finally:
        connection.rollback()
        cursor.close()
        connection.close()

@pytest.fixture
def delete_user_by_phone_from_db_session(marketplace_db_session):
    def _delete(phone):
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
    return _delete


@pytest.fixture
def catalog_headers_simple(generate_jwt_token_catalog):
    headers = (
        Headers_catalog()
        .with_x_api_key(generate_jwt_token_catalog)
        .with_cns_agent("Web CNS Fix-Price")
        .build()
    )
    return headers

@pytest.fixture
def client_catalog_create():
    clients=Authorization_Catalog()
    return clients