import allure
import pytest

from clients.api.V2.authorization import Authotization
from tests.test_V2.models import Login
from clients.api.helpers.helpers import Models_Pydantic,Checking
from clients.api.helpers.helpers_db import SessionDbHelper


@pytest.mark.parametrize("phone,password,x_city,status_code", [
    
    ("79156789834", "Hf,jnf45", "3",200),
    ("375787878991","Hf,jnf45","14",200)
    ])

@allure.title("Позитивная авторизация")
def test_login(session_non_authorized_x_key, phone, password, x_city,status_code,cursor_db_session):
    session,x_key = session_non_authorized_x_key
    hash=x_key.split(":")[1]
    headers = {
        "x-city": x_city,
        "x-key": x_key
    }
    body = {
        "phone": phone,
        "password": password
    }

    res =Authotization.post_auth_login(session=session,json=body,headers=headers)

    user_data=Models_Pydantic.validate_response(res.json(),Login)
    Checking.assert_status_code(res,status_code)

    with allure.step("Проверка содержания ответа"):
        assert user_data.isUserConfirmed==False

    SessionDbHelper.checking_session_login_buyer_in_session_db(cursor_db_session, hash)






