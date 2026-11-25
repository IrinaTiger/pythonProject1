import pytest
from clients.api.helpers.helpers import Checking, Models_Pydantic
from clients.api.marketplace.v1.auth.models import AuthConfirmRegistrationResponse
from faker import Faker
import allure


fake=Faker()
@allure.title("Проверка кода регистрации у {phone}")
@pytest.mark.parametrize("phone,x_city,country",[
    (fake.numerify("79#########"),"3","RU"),
    (fake.numerify("77#########"),"1729","KZ"),
    (fake.numerify("375#########"),"14","BY"),
    (fake.numerify("371########"),"685","LV")

])
def test_phone_registration_auth_confirm(send_registration_code,auth_confirm_registration_marketplace,phone,
                                         db_session_log_confirm_by_phone,
                                         db_session_confirm_request_by_phone
                                         ):

    code=send_registration_code
    response=auth_confirm_registration_marketplace.auth_confirm_registration(phone=phone,code=code)
    Checking.assert_status_code(response, 200)
    registration_response=Models_Pydantic.validate_response(response.json(),AuthConfirmRegistrationResponse)
    assert registration_response.action =="showRegistrationForm"
    expected_log_confirm={"type": "registration", "recipient": phone, "channel": "sms","code_inserted":code, "phone": phone}
    log_confirm=db_session_log_confirm_by_phone(phone,expected_log_confirm)
    expected_confirm_request={"type": "registration", "recipient": phone, "channel": "sms","code":code, "phone": phone}
    confirm_request= db_session_confirm_request_by_phone(phone,expected_confirm_request)


