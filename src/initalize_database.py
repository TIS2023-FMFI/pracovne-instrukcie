import os

from constants import INSTRUCTIONS_DIR
from database_manager import DBManager

db = DBManager()
db.run_script('initialize_database.sql')

for root, dirs, files in os.walk(INSTRUCTIONS_DIR):
    for file in files:
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)

            instruction = (file.removesuffix('.pdf'), file_path, '2024-07-25')
            db.execute_query(f"INSERT INTO instructions (name, file_path, expiration_date) "
                             f"VALUES {instruction}; ")
