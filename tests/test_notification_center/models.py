import pytest
from pydantic import BaseModel,TypeAdapter
import allure
from  clients.api.helpers.helpers import Models_Pydantic
from typing import List



class GetNotification(BaseModel):

    orderId:int
    combinedOrderId: str
    title: str
    date: str
    time: str
    type: str
    unreadMessages: int



class  ValiditeNotification(Models_Pydantic):
    @staticmethod
    def validate_list_response(response):
       return Models_Pydantic.validate_list_response(response,GetNotification)
class GET_Notification_id(BaseModel):
    date:str
    time:str
    status:str
    message:str


@allure.step("Валидация ответа")
def validate_get_notification_id(response):

    try:
        notification_id=[GET_Notification_id.model_validate(notification) for notification in response.json()]
        return notification_id
    except ValueError as e:
        pytest.fail(f"Валидация не прошла {e}")


