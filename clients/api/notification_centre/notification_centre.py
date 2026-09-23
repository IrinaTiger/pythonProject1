import os
import allure
from dotenv import load_dotenv
import requests
load_dotenv()
BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")
from clients.api_clients import  ApiClient

class NotificationV1(ApiClient):
    def __init__(self):
        super().__init__(f"{BASE_URL_NOTIFICATION_CENTER}/v1/")


    @allure.title('Получение уведомлений')
    def get_notification(self,headers=None):
        endpoint="/notification"
        response=self.get(endpoint,headers=headers)
        return response


    @allure.title("Получение уведомлений по id")
    def get_notification_id(self,id,headers=None,timeout=None):
        endpoint=f"/notification/order/{id}"
        response=self.get(endpoint, headers=headers)
        return response










