import os
from dotenv import load_dotenv
load_dotenv()
from curlify import to_curl
import allure
from tests.test_notification_center.models import validate_get_notification_id,ValiditeNotification
from clients.api.notification_centre.notification_centre import NotificationV1

BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")




def test_get_notification(generate_jwt_token,db_notification_centre,get_headers):

    with allure.step("Поиск рандомного buyer"):
        db_notification_centre.execute(f'select buyer_id from public.notification limit 1')
        buyer_id=db_notification_centre.fetchone()[0]

    with allure.step("Формирование заголовков для теста"):
        headers=get_headers(
            buyer_id=buyer_id,
            jwt_token=generate_jwt_token,
            language='ru'
        )
    client=NotificationV1()

    response=client.get_notification(headers=headers)
    allure.attach(to_curl(response.request),
                  name="Curl GET /notification",
                  attachment_type=allure.attachment_type.JSON
                  )

    assert response.status_code==200
    ValiditeNotification.validate_list_response(response.json()



def test_get_notification_id(generate_jwt_token,get_headers,db_notification_centre):
    db_notification_centre.execute("SELECT buyer_id,payload->>'orderId' from public.notification where type= 'order' limit 1")
    buyer_id, order_id =db_notification_centre.fetchone()
    order_id=str(order_id.split('-')[1]) if "-" in order_id else order_id
    headers=get_headers(
        buyer_id=buyer_id,
        jwt_token = generate_jwt_token
    )
    clients=NotificationV1()

    response=clients.get_notification_id(id=order_id,headers=headers,timeout=1)
    assert response.status_code==200
    allure.attach(to_curl(response.request),
                   name="Curl GET notificatuion/{id}",
                   attachment_type=allure.attachment_type.JSON
                   )
    validate_get_notification_id(response)

