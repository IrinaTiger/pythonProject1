
class Headers_marketplace:
    def __init__(self):
        self._headers={}

    def with_x_key(self,x_key):
        self._headers["x-key"]=x_key
        return self

    def with_x_city(self,x_city):
        self._headers["x-city"]=str(x_city)
        return self

    def with_x_pfm(self,x_pfm):
        self._headers["x-pfm"]=x_pfm
        return self

    def with_x_language(self,x_language):
        self._headers["x-language"]=x_language
        return self

    def with_buyer_id(self,buyer_id):
        self._headers["buyer-id"]=str(buyer_id)
        return self

    def with_jwt_token(self,jwt_token):
        self._headers["jwt-token"]=jwt_token
        return self

    def build(self):
        return self._headers


class Headers_catalog:
    def __init__(self):
        self.headers = {}

    def with_cns_agent(self, cns_agent):
        self.headers["Cns-Agent"] = cns_agent
        return self

    def with_x_api_key(self, x_api_key):
        self.headers["X-Api-key"] = x_api_key
        return self

    def with_x_country(self, x_country):
        self.headers["X-Country"] = x_country
        return self

    def with_x_language(self, x_language):
        self.headers["X-Language"] = x_language
        return self

    def build(self):
        return self.headers