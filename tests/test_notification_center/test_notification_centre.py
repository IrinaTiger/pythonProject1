import os
from dotenv import load_dotenv
load_dotenv()
import pytest
import requests
from curlify import to_curl


from api.notification_centre.notification_centre import Notification_v1

BASE_URL_NOTIFICATION_CENTER=os.getenv("BASE_URL_NOTIFICATION_CENTER")


def test_get_notification(generate_jwt_token,db_notification_centre):
    object=Notification_v1(base_url=BASE_URL_NOTIFICATION_CENTER)
    db_notification_centre.execute(f'select buyer_id from public.notification limit 1')
    buyer_id=db_notification_centre.fetchone()

    headers=object.get_headers(jwt_token=generate_jwt_token, buyer_id=buyer_id)

    response=object.get_notification(headers=headers)

    assert response.status_code==200
