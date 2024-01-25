import sqlite3


class DBManager:
    def __init__(self, database_name: str = 'database.db') -> None:
        self.database_name: str = database_name

    def execute_query(self, query):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result

    def run_script(self, script_file: str) -> None:
        conn = sqlite3.connect(self.database_name)

        with open(script_file, 'r', encoding='utf=8') as sf:
            script = sf.read()
            conn.executescript(script)

        conn.commit()
        conn.close()


if __name__ == '__main__':
    db = DBManager()
    db.run_script('create_script.sql')
