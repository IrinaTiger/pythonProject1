import os

import allure
from dotenv import load_dotenv
import requests
load_dotenv()
import allure

BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")

class Notification_v1:

    base_url=f"{BASE_URL_NOTIFICATION_CENTER}/v1/"

    @staticmethod
    @allure.title('Получение уведомлений')
    def get_notification(headers=None):
        url=f"{Notification_v1.base_url}notification"

        response=requests.get(url,headers=headers)
        return response

    @staticmethod
    @allure.title("Получение уведомлений по id")
    def get_notification_id(id,headers=None):
        url=f"{Notification_v1.base_url}notification/order/{id}"
        response=requests.get(url, headers=headers)
        return response










