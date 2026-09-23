from pydantic import BaseModel,TypeAdapter
from pydantic import ValidationError
import pytest
import allure
from typing import List
class Models_Pydantic(BaseModel):
    @staticmethod
    @allure.step("Проверка схемы валидации")
    def validate_response(response_model,model):
        try:
            return model.model_validate(response_model)
        except ValueError as e:
            pytest.fail(f"Параметр ответа не соответствует схесе {e}")

    @staticmethod
    @allure.step("Проверка схемы валидации")
    def validate_list_response(response_model, model):
        try:
            adapter=TypeAdapter(List[model])
            return adapter.validate_python(response_model)
        except ValueError as e:
            pytest.fail(f"Параметр ответа не соответствует схесе {e}")



class Checking:

    @staticmethod
    @allure.step("Проверка стутус-кода")
    def assert_status_code(response,expected_status_code):
        assert response.status_code==expected_status_code,f"Статус код {response.status_code} не равен ожидаемому{expected_status_code}"





