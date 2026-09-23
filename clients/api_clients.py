import requests
from urllib.parse import urljoin
import allure

class ApiClient:
    def __init__(self,base_url):
        self.base_url=base_url
        self.session=requests.Session()
        with allure.step(f"Создание клиента {base_url}"):
            pass


    @allure.step("Вызывается метод GET c {endpoint}")
    def get(self,endpoint,headers=None,params=None):
        url=urljoin(self.base_url,endpoint.lstrip("/"))
        response = self.session.get(url, params=params, headers=headers)

        allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        return response

    def post(self,endpoint,headers=None,params=None,json=None,data=None):
        url=urljoin(self.base_url,endpoint.lstrip("/"))
        return self.session.post(url,headers=headers,params=params,json=json,data=data)

    def put(self,endpoint,params=None,headers=None,json=None,data=None):
        url=urljoin(self.base_url,endpoint.lstrip("/"))
        return self.session.put(url,params=params,headers=headers,json=json,data=data)