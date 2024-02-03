import datetime

from database_manager import DBManager


class History:
    def __init__(self) -> None:
        self.database: DBManager = DBManager()

    def log_open_instruction(self, user_id: str, instruction_id: str) -> None:
        self.database.execute_query(f"DELETE FROM history "
                                    f"WHERE username='{user_id}' AND instruction_id='{instruction_id}'")

        self.database.execute_query(f"INSERT INTO history (username, instruction_id) "
                                    f"VALUES ('{user_id}', '{instruction_id}')")

    def get_user_history(self, user_id: str) -> list[int]:
        return [
            int(instruction[0])
            for instruction in self.database.execute_query(f"SELECT instruction_id FROM history "
                                                           f"WHERE username = '{user_id}' "
                                                           f"ORDER BY id DESC ")
        ]
