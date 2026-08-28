from pydantic import BaseModel
from pydantic import ValidationError
import pytest
import allure

class Models_Pydantic(BaseModel):
    @staticmethod
    @allure.step("Проверка схемы валидации")
    def validate_response(response_model,model):
        try:
            return model.model_validate(response_model)
        except ValueError as e:
            pytest.fail(f"Параметр ответа не соответствует схесе {e}")



class Checking:

    @staticmethod
    @allure.step("Проверка стутус-кода")
    def assert_status_code(response,expected_status_code):
        assert response.status_code==expected_status_code,f"Статус код {response.status_code} не равен ожидаемому{expected_status_code}"




