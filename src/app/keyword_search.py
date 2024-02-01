import PyPDF2
import os
from unidecode import unidecode


class Search:
    def __init__(self, directory_path: str) -> None:
        self.instructions_dir = directory_path
        self.words_in_pdf: dict[str, set[str]] = dict()
        self.preread_pdfs()

    def preread_pdfs(self) -> None:
        for instruction in os.listdir(self.instructions_dir):
            if instruction.endswith('.pdf'):
                self.read_pdf(instruction)

    def read_pdf(self, instruction: str) -> None:
        set_of_words: set[str] = set()
        for word in instruction.split():
            set_of_words.add(unidecode(word.lower()))

        pdfFileObj = open(self.instructions_dir + instruction, 'rb')
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

    def filter_instructions(self, keyword: str = '', user_history: tuple[str] = ()) -> list[str]:
        instructions: list[str] = [
            instruction.removesuffix('.pdf')
            for instruction in os.listdir(self.instructions_dir)
            if instruction.endswith('.pdf') and self.contains_keyword(instruction, unidecode(keyword.lower()))
        ]

        output: list[str] = []
        for instruction in user_history:
            if instruction in instructions:
                output.append(instruction)
                instructions.remove(instruction)

        return output + instructions
