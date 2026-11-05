from clients.api.v1.authorization.Facades.FacadesV1.FacadeAuthorization import FacadeAuthorization

import pytest
from clients.api.v1.authorization.authorization_client import Authorization
from clients.api.helpers.helpers_db import SessionDbHelper



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


@pytest.fixture
def client_marketplace_Authorization():
    client=Authorization()
    return client

@pytest.fixture
def auth_request_marketplace(client_marketplace_Authorization,session_non_authorized_x_key,get_headers,x_city):
    _, x_key = session_non_authorized_x_key

    headers = get_headers(x_key=x_key,x_city=x_city)
    return FacadeAuthorization(client_marketplace_Authorization,headers)


@pytest.fixture
def check_config_ecom_new_auth_sms_email_expire(marketplace_db):
    marketplace_db.execute("select value from public.config "
                            "where alias ='ecom.new.auth.sms.email.expire'")

    value=marketplace_db.fetchone()
    print(value)
    if value != (3600,):
        marketplace_db.execute("UPDATE public.config "
                               "SET value='3600' "
                               "where alias ='ecom.new.auth.sms.email.expire'")

    marketplace_db.connection.commit()
    yield
    marketplace_db.connection.rollback()