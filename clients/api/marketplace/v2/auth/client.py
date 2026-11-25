import os
import pytest
import requests
import allure
from curlify import to_curl

class Authotization:

    BASE_URL=os.getenv("BASE_URL")

    @staticmethod
    @allure.step("Вызываем апи POST авторизацию ")
    def post_auth_login(session=None,json=None,headers=None):
        url=f"{Authotization.BASE_URL}/buyer/v2/auth/login"
        res=session.post(url,json=json,headers= headers)
        allure.attach(
            to_curl(res.request),
            name="cURL запрос",
            attachment_type=allure.attachment_type.JSON
        )
        return res
        



