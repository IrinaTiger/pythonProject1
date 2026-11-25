from clients.api.marketplace.v1.auth.facade import FacadeAuthorization, FacadeRegistration
import pytest
from clients.api.marketplace.v1.auth.client import Authorization
from clients.api.helpers.helpers import Checking, Models_Pydantic
from clients.api.marketplace.v1.auth.models import AuthRequestResponse


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
def sms_repeat_config_60(check_config_ecom):
    return (check_config_ecom("ecom.new.auth.sms.repeat", 60))

@pytest.fixture
def sms_expire_config_3600(check_config_ecom):
    return check_config_ecom("ecom.new.auth.sms.email.expire", 3600)

@pytest.fixture
def email_repeat_config_60(check_config_ecom):
    return check_config_ecom('ecom.new.auth.email.repeat',60)

@pytest.fixture
def sms_registration_repeat_config(check_config_ecom):
    return check_config_ecom("ecom.new.registration.sms.repeat",60)

@pytest.fixture
def sms_registration_expire_config(check_config_ecom):
    return check_config_ecom("ecom.new.registration.sms.expire",3600)

@pytest.fixture
def send_registration_code(sms_registration_repeat_config,
                                                sms_registration_expire_config,
                                                user_not_exist_in_catalog,
                                                phone,
                                                auth_request_marketplace,
                                                db_session_log_confirm_by_phone,
                                                db_session_confirm_request_by_phone):
    response = auth_request_marketplace.auth_request(phone=phone)
    Checking.assert_status_code(response, 200)
    auth_response = Models_Pydantic.validate_response(response.json(), AuthRequestResponse)
    assert auth_response.action == 'enterCode'
    assert auth_response.expireTime == sms_registration_expire_config
    assert auth_response.repeatTime == sms_registration_repeat_config
    assert auth_response.channel.type == 'sms'
    assert auth_response.channel.value == phone
    expected_data_db = {"type": "registration", "recipient": phone, "channel": "sms", "phone": phone}
    log_confirm = db_session_log_confirm_by_phone(phone, expected_data_db)
    confirm_request = db_session_confirm_request_by_phone(phone, expected_data_db)
    return log_confirm["code"]


@pytest.fixture
def auth_confirm_registration_marketplace(client_marketplace_Authorization,session_non_authorized_x_key,get_headers,x_city):
    _, x_key = session_non_authorized_x_key

    headers = get_headers(x_key=x_key,x_city=x_city)
    return FacadeRegistration(client_marketplace_Authorization, headers)