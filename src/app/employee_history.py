import datetime

from database_manager import DBManager


class History:
    def __init__(self) -> None:
        self.database: DBManager = DBManager()

    def log_open_instruction(self, user_code: str, instruction_id: str) -> None:
        self.database.execute_query(f"DELETE FROM history "
                                    f"WHERE user_code='{user_code}' AND instruction_id='{instruction_id}'")

        self.database.execute_query(f"INSERT INTO history (user_code, instruction_id) "
                                    f"VALUES ('{user_code}', '{instruction_id}')")

    def get_user_history(self, user_code: str) -> list[int]:
        return [
            int(instruction[0])
            for instruction in self.database.execute_query(f"SELECT instruction_id FROM history "
                                                           f"WHERE user_code = '{user_code}' "
                                                           f"ORDER BY id DESC ")
        ]
