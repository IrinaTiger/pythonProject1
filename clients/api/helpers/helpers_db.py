import allure
import pytest

class SessionDbHelper():

    @classmethod
    @allure.step("Проверка, что данные занесены в buyer.session c buyer_id")

    def checking_session_login_buyer_in_session_db(cursor,hash):
        cursor.execute("SELECT* from buyer.session where hash=%s", (hash,))
        assert cursor.fetchone() is not None
        cursor.execute("SELECT logged,buyer_id from buyer.session where hash=%s", (hash,))
        assert cursor.fetchone() is not None

    @staticmethod
    @allure.step("Проверка записи в buyer.log_confirm для телефона {phone}")
    def checking_session_log_confirm_by_phone(marketplace_db_session,phone,expected_data):
        marketplace_db_session.execute("SELECT type,recipient,code,code_inserted,channel,phone from buyer.log_confirm "
                                       "where phone=%s order by id desc limit 1",
                                       (phone,))

        row=marketplace_db_session.fetchone()
        assert row is not None, f"В log_confirm нет записей для {phone}"

        actual={}
        for key in expected_data:
            actual[key]=row[key]

        assert expected_data==actual, f"Данные в log_confirm не совпадают: {actual}"
        return row

    @staticmethod
    @allure.step("Проверка записи в buyer.confirm_request для телефона {phone}")
    def checking_session_confirm_request_by_phone(marketplace_db_session,phone,expected_data):
        marketplace_db_session.execute("SELECT type,recipient,code,channel,phone,user_payload from buyer.confirm_request "
                                       "where phone=%s order by id desc limit 1",
                                       (phone,))

        row=marketplace_db_session.fetchone()
        assert row is not None, f"В confirm_request нет записей для {phone}"
        actual={}

        for key in expected_data:
            actual[key]=row[key]


        assert expected_data == actual, f"Данные в confirm_request не совпадают: {actual}"
        return row