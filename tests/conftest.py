
import pytest


@pytest.fixture
def get_headers():
    def _get_headers(x_key=None,jwt_token=None, buyer_id=None, language=None,x_city=None):

        headers = {}

        if jwt_token:
            headers["Token"] = jwt_token
        if buyer_id:
            headers["X-Buyer-Id"] = str(buyer_id)
        if language:
            headers["X-Language"] = language
        if x_key:
            headers["X-Key"]=x_key
        if x_city:
            headers["X-city"]=x_city

        return headers
    return _get_headers


