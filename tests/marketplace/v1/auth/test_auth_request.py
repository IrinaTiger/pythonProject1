import pytest
import allure
from clients.api.helpers.helpers import Checking, Models_Pydantic
from clients.api.marketplace.v1.auth.models import AuthRequestResponse
from faker import Faker



fake=Faker()
#тест - идем в каталог- смотрим, что по телефону есть пользак
#идем в маркет - вход

@allure.title("Запрос на отправку кода авторизации по смс {country} для пользователя из каталога")
@pytest.mark.parametrize("phone,x_city,country,email",[
  ("77880000006","1729","KZ","demo9@last.kz"),
  ("79163435333","3","RU","12212@mail.ru"),

  ("37144654656","685","LV","blacknigwwa311@gmail.com"),
    ("375323232344","14","BY","blackni22ga311@gmail.com"),


])
def test_auth_request_sms_for_catalog_user( email_repeat_config_60,
                                           sms_expire_config_3600,
                                            user_exist_in_catalog,
                                            delete_user_by_phone_from_db_session,
                                            phone,email,
                                            auth_request_marketplace,db_session_log_confirm_by_phone,
                                            db_session_confirm_request_by_phone):

    #запрос в catalog-buyer найден(200)- авторизация в маркет
    #Проверки: тип,значение данных, занесение в бд

    response=auth_request_marketplace.auth_request(phone=phone)
    Checking.assert_status_code(response, 200)
    auth_response = Models_Pydantic.validate_response(response.json(), AuthRequestResponse)
    assert auth_response.repeatTime == email_repeat_config_60, f" expireTime !=60"
    assert auth_response.expireTime==sms_expire_config_3600,f" expireTime !=3600"
    assert auth_response.action=="enterCode"
    assert auth_response.channel.type=="email"
    expected= {"type": "auth", "recipient": email, "channel": "email", "phone": phone}
    log_confirm=db_session_log_confirm_by_phone(phone, expected)
    confirm_request=db_session_confirm_request_by_phone(phone,expected)


@allure.title("Запрос на отправку кода регистрации по смс {country} для пользователя из каталога")
@pytest.mark.parametrize("phone,x_city,country",[
    (fake.numerify("79#########"),"3","RU"),
    (fake.numerify("77#########"),"1729","KZ"),
    (fake.numerify("375#########"),"14","BY"),
    (fake.numerify("371########"),"685","LV")

])
def test_auth_request_sms_for_not_catalog_user( sms_registration_repeat_config,
                                                sms_registration_expire_config,
                                                user_not_exist_in_catalog,
                                                phone,
                                                auth_request_marketplace,
                                                db_session_log_confirm_by_phone,
                                                db_session_confirm_request_by_phone):
    # запрос в catalog-buyer НЕ найден(400)- регистрация в маркет
    # Проверки: тип,значение данных, занесение в бд

    response=auth_request_marketplace.auth_request(phone=phone)
    Checking.assert_status_code(response, 200)
    auth_response = Models_Pydantic.validate_response(response.json(), AuthRequestResponse)
    assert auth_response.action=='enterCode'
    assert auth_response.expireTime==  sms_registration_expire_config
    assert auth_response.repeatTime==sms_registration_repeat_config
    assert auth_response.channel.type=='sms'
    assert auth_response.channel.value==phone
    expected_data_db={"type": "registration", "recipient": phone, "channel": "sms", "phone": phone}
    log_confirm = db_session_log_confirm_by_phone(phone, expected_data_db)
    confirm_request = db_session_confirm_request_by_phone(phone, expected_data_db)






