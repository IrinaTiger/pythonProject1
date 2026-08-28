import os
from dotenv import load_dotenv
import requests
load_dotenv()

BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")

class Notification_v1:
    def __init__ (self,base_url):
        self.base_url=f"{BASE_URL_NOTIFICATION_CENTER}/v1/"


    def get_headers(self,jwt_token=None,buyer_id=None,language=None):
        headers={}

        if jwt_token:
            headers["Token"]=jwt_token
        if buyer_id:
            headers["X-Buyer-Id"]=str(buyer_id)
        if language:
            headers["X-Language"]=language

        return headers

    def get_notification(self,headers=None):
        url=f"{self.base_url}notification"

        response=requests.get(url,headers=headers)
        return response







