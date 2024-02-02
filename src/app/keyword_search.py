import PyPDF2
import os
from unidecode import unidecode

from constants import INSTRUCTIONS_DIR
from instruction import Instruction


class Search:
    def __init__(self) -> None:
        self.words_in_pdf: dict[str, set[str]] = dict()
        # TODO: read PDFs at startup
        # self.preread_pdfs()

    def preread_pdfs(self) -> None:
        for instruction in os.listdir(INSTRUCTIONS_DIR):
            if instruction.endswith('.pdf'):
                self.read_pdf(instruction.removesuffix('.pdf'))

    def read_pdf(self, instruction: str) -> None:
        set_of_words: set[str] = set()
        for word in instruction.split():
            set_of_words.add(unidecode(word.lower()))

        pdfFileObj = open(INSTRUCTIONS_DIR + instruction + '.pdf', 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            pageObj = pdfReader.pages[i]

            for word in pageObj.extract_text().split():
                set_of_words.add(unidecode(word.lower()))

        pdfFileObj.close()

        self.words_in_pdf[instruction] = set_of_words

    def contains_keyword(self, instruction: str, keyword: str = '') -> bool:
        if keyword == '':
            return True

        if instruction not in self.words_in_pdf:
            self.read_pdf(instruction)

        for word in self.words_in_pdf[instruction]:
            if word.startswith(keyword):
                return True

        return False

    def filter_instructions(self, keyword: str, history: tuple[int], all_instructions: list[Instruction]) -> list[Instruction]:
        instructions: list[Instruction] = list()
        for _id in all_instructions:
            if self.contains_keyword(_id.name, unidecode(keyword.lower())):
                instructions.append(_id)

        instruction_ids: dict[int, Instruction] = {instr.id: instr for instr in instructions}
        output: list[Instruction] = list()
        for _id in history:
            if _id in instruction_ids.keys():
                output.append(instruction_ids[_id])
                instructions.remove(instruction_ids[_id])
                del instruction_ids[_id]

        return output + instructions
