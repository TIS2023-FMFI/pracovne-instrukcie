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
        #  self.preread_pdfs()

    def preread_pdfs(self) -> None:
        instructions_list = self.database.execute_query(f"SELECT file_path, name FROM instructions")
        for instruction_path, name in instructions_list:
            if instruction_path.endswith('.pdf'):
                self.read_pdf(instruction_path, name)

    def read_pdf(self, instruction_path: str, name: str) -> None:
        if not os.path.exists(instruction_path):
            return

        set_of_words: set[str] = set()
        path_split = instruction_path.rsplit('/', 1)[-1].removesuffix('.pdf').split()
        for word in path_split + name.split():
            set_of_words.add(unidecode(word.lower()))

        pdfFileObj = open(instruction_path, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            pageObj = pdfReader.pages[i]

            for word in pageObj.extract_text().split():
                set_of_words.add(unidecode(word.lower()))

        pdfFileObj.close()

        self.words_in_pdf[instruction_path] = set_of_words

    def contains_keyword(self, instruction: Instruction, keyword: str = '') -> bool:
        if keyword == '':
            return True

        if instruction.file_path not in self.words_in_pdf:
            self.read_pdf(instruction.file_path, instruction.name)

        for word in self.words_in_pdf[instruction.file_path]:
            if word.startswith(keyword):
                return True

        return False

    def filter_instructions(self, keyword: str, history: tuple[int], all_instructions: list[Instruction]) -> list[
        Instruction]:
        instructions: list[Instruction] = list()
        for instruction in all_instructions:
            if self.contains_keyword(instruction, unidecode(keyword.lower())):
                instructions.append(instruction)

        instruction_ids: dict[int, Instruction] = {instr.id: instr for instr in instructions}
        output: list[Instruction] = list()
        for instruction in history:
            if instruction in instruction_ids.keys():
                output.append(instruction_ids[instruction])
                instructions.remove(instruction_ids[instruction])
                del instruction_ids[instruction]

        return output + instructions
