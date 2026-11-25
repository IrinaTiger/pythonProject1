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
        return response


class FacadeRegistration:
    def __init__(self,client,headers):
        self.client=client
        self.headers=headers

    def auth_confirm_registration(self,code,phone):

            body={
                "code": str(code),
                "channel": "sms",
                "phone": phone

            }
            response=self.client.auth_confirm(json=body,headers=self.headers)
            return response
