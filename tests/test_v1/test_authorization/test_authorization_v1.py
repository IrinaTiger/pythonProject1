import pytest
import allure
from clients.api.helpers.helpers import Checking, Models_Pydantic
from tests.test_v1.test_authorization.authorization_models import AuthRequestResponse


#тест - идем в каталог- смотрим, что по телефону есть пользак
#идем в маркет - вход

@allure.title("Запрос на отправку кода атворизации по смс RU для пользователя из каталога")
@pytest.mark.parametrize("phone,x_city",[
  ("79154004274","3")


])
def test_auth_request_sms_for_catalog_user(user_exist_in_catalog_ru,
                          delete_user_by_phone_from_db_session,
                          phone,
                          auth_request_marketplace,db_session_log_confirm_by_phone,
                          db_session_confirm_request_by_phone,check_config_ecom_new_auth_sms_email_expire):

    #запрос в catalog-buyer найден(200)- авторизация в маркет

    response=auth_request_marketplace.auth_request(phone=phone)
    Checking.assert_status_code(response, 200)

    auth_response=Models_Pydantic.validate_response(response.json(),AuthRequestResponse)
    assert auth_response.expireTime==3600,f" expireTime !=3600"
    expected= {"type": "auth", "recipient": phone, "channel": "sms", "phone": phone}
    log_confirm=db_session_log_confirm_by_phone(phone, expected)
    confirm_request=db_session_confirm_request_by_phone(phone,expected)





