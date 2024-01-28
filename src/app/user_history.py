import datetime

from database_manager import DBManager


class History:
    def __init__(self) -> None:
        self.database: DBManager = DBManager()

    def log_open_instruction(self, user_id: str, name_of_instruction: str) -> None:
        self.database.execute_query(f"DELETE FROM history "
                                    f"WHERE username='{user_id}' AND instruction_name='{name_of_instruction}'")

        self.database.execute_query(f"INSERT INTO history (username, instruction_name) "
                                    f"VALUES ('{user_id}', '{name_of_instruction}')")

    def get_user_history(self, user_id: str) -> List[str]:
        return [
            instruction[0]
            for instruction in self.database.execute_query(f"SELECT instruction_name FROM history "
                                                           f"WHERE username = '{user_id}' "
                                                           f"ORDER BY id DESC ")
        ]
