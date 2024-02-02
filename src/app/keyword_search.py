import PyPDF2
import os
from unidecode import unidecode

from constants import INSTRUCTIONS_DIR
from instruction import Instruction

from database_manager import DBManager

class Search:
    def __init__(self) -> None:
        self.words_in_pdf: dict[str, set[str]] = dict()
        self.database: DBManager = DBManager()
        # TODO: read PDFs at startup
        self.preread_pdfs()

    def preread_pdfs(self) -> None:
        instructions_list_path = [instr[0] for instr in self.database.execute_query(f"SELECT file_path FROM instructions")]
        for instruction_path in instructions_list_path:
            if instruction_path.endswith('.pdf') and os.path.exists(instruction_path):
                self.read_pdf(instruction_path)

    def read_pdf(self, instruction_path: str) -> None:
        set_of_words: set[str] = set()
        for word in instruction_path.split():
            set_of_words.add(unidecode(word.lower()))

        pdfFileObj = open(instruction_path, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            pageObj = pdfReader.pages[i]

            for word in pageObj.extract_text().split():
                set_of_words.add(unidecode(word.lower()))

        pdfFileObj.close()

        self.words_in_pdf[instruction_path] = set_of_words

    def contains_keyword(self, path: str, keyword: str = '') -> bool:
        if keyword == '':
            return True

        if path not in self.words_in_pdf:
            self.read_pdf(path)

        for word in self.words_in_pdf[path]:
            if word.startswith(keyword):
                return True

        return False

    def filter_instructions(self, keyword: str, history: tuple[int], all_instructions: list[Instruction]) -> list[Instruction]:
        instructions: list[Instruction] = list()
        for _id in all_instructions:
            if self.contains_keyword(_id.file_path, unidecode(keyword.lower())):
                instructions.append(_id)

        instruction_ids: dict[int, Instruction] = {instr.id: instr for instr in instructions}
        output: list[Instruction] = list()
        for _id in history:
            if _id in instruction_ids.keys():
                output.append(instruction_ids[_id])
                instructions.remove(instruction_ids[_id])
                del instruction_ids[_id]

        return output + instructions
