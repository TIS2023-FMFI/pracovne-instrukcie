from database_manager import DBManager


class Instruction:
    def __init__(self, _id, name, file_path, validation_date, expiration_date):
        self.id = _id
        self.name = name
        self.file_path = file_path
        self.validation_date = validation_date
        self.expiration_date = expiration_date


def initialize_instructions() -> list[Instruction]:
    database = DBManager()
    out: list[Instruction] = list()

    instruction_list: list[tuple] = database.execute_query(f"SELECT * FROM instructions")
    for instruction in instruction_list:
        out.append(Instruction(*instruction))

    return out
