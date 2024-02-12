import os

from constants import INSTRUCTIONS_DIR
from database_manager import DBManager

valid_until = '2024-09-01'

db = DBManager()
db.run_script('initialize_database.sql')

all_paths = [path[0] for path in db.execute_query("SELECT file_path FROM instructions")]
print(*all_paths, sep='\n')

for root, dirs, files in os.walk(INSTRUCTIONS_DIR):
    for file in files:
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)
            if file_path not in all_paths:
                instruction = (file.removesuffix('.pdf'), file_path, valid_until)
                db.execute_query(f"INSERT INTO instructions (name, file_path, expiration_date) "
                                 f"VALUES {instruction}; ")
