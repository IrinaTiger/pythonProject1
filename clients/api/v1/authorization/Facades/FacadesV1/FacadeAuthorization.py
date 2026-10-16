from clients.api.v1.authorization.authorization_client import Authorization
from clients.api.helpers.helpers import Checking
class FacadeAuthorization:
    def __init__(self,client,headers):
        self.client=client
        self.headers=headers

    def auth_request(self,phone):

        body = {
            "phone": phone,
            "captcha": ""
        }
        response = self.client.auth_request(json=body, headers=self.headers)
        Checking.assert_status_code(response, 200)
        return response