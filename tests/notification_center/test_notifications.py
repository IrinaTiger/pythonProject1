import os
from dotenv import load_dotenv
load_dotenv()
from curlify import to_curl
import allure
from clients.api.notification_center.models import NotificationItem, NotificationDetails
from clients.api.helpers.helpers import Models_Pydantic
from clients.api.notification_center.client import NotificationV1

BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")




def test_get_notification(generate_jwt_token_notification_center,db_notification_centre,get_headers):

    with allure.step("Поиск рандомного buyer"):
        db_notification_centre.execute(f'select buyer_id from public.notification limit 1')
        buyer_id=db_notification_centre.fetchone()[0]

    with allure.step("Формирование заголовков для теста"):
        headers=get_headers(
            buyer_id=buyer_id,
            jwt_token=generate_jwt_token_notification_center,
            language='ru'
        )
    client=NotificationV1()

    response=client.get_notification(headers=headers)

    assert response.status_code==200
    Models_Pydantic.validate_list_response(response.json(), NotificationItem)



def test_get_notification_id(generate_jwt_token_notification_center,get_headers,db_notification_centre):
    db_notification_centre.execute("SELECT buyer_id,payload->>'orderId' from public.notification where type= 'order' limit 1")
    buyer_id, order_id =db_notification_centre.fetchone()
    order_id=str(order_id.split('-')[1]) if "-" in order_id else order_id
    headers=get_headers(
        buyer_id=buyer_id,
        jwt_token = generate_jwt_token_notification_center,
        language='ru'
    )
    clients=NotificationV1()

    response=clients.get_notification_id(id=order_id,headers=headers,timeout=1)
    assert response.status_code==200

    Models_Pydantic.validate_list_response(response.json(), NotificationDetails)

