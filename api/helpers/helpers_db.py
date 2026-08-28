import allure
import pytest

class SessionDbHelper():

    @staticmethod
    @allure.step("Проверка, что данные занесены в buyer.session c buyer_id")

    def checking_session_login_buyer_in_session_db(cursor,hash):
        cursor.execute("SELECT* from buyer.session where hash=%s", (hash,))
        assert cursor.fetchone() is not None
        cursor.execute("SELECT logged,buyer_id from buyer.session where hash=%s", (hash,))
        assert cursor.fetchone() is not None
