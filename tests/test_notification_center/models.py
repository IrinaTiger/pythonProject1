import pytest
from pydantic import BaseModel
import allure



class GET_Notification(BaseModel):

    orderId:int
    combinedOrderId: str
    title: str
    date: str
    time: str
    type: str
    unreadMessages: int



@allure.step("Валидация ответа")
def validate_get_notification(response):

    notifications = [GET_Notification.model_validate(notification) for notification in response.json()]
    return notifications

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


