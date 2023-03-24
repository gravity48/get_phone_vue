import io
import six
import msoffcrypto
import xlrd
from xlrd.book import Book
from .abc import BaseTextHandler, ProcessOpenHandler


class XlrdHandler(BaseTextHandler):

    def __init__(self, filepath):
        super(XlrdHandler, self).__init__(filepath)

    def _decrypt_file(self) -> io.BytesIO:
        with open(self.filepath, 'rb') as f:
            file_ = io.BytesIO(f.read())
        ms_file = msoffcrypto.OfficeFile(file_)
        ms_file.load_key(password='VelvetSweatshop')
        decrypted = io.BytesIO()
        ms_file.decrypt(decrypted)
        del file_
        return decrypted

    def _open_workbook(self) -> Book:
        try:
            workbook: Book = xlrd.open_workbook(filename=self.filepath)
            return workbook
        except xlrd.XLRDError as e:
            if str(e) == 'Workbook is encrypted':
                workbook: Book = xlrd.open_workbook(file_contents=self._decrypt_file())
                return workbook
            raise xlrd.XLRDError(str(e))

    @staticmethod
    def extract_text(workbook: Book) -> str:
        sheets_name = workbook.sheet_names()
        output = "\n"
        for names in sheets_name:
            worksheet = workbook.sheet_by_name(names)
            num_rows = worksheet.nrows
            num_cells = worksheet.ncols
            for curr_row in range(num_rows):
                row = worksheet.row(curr_row)
                new_output = []
                for index_col in range(num_cells):
                    value = worksheet.cell_value(curr_row, index_col)
                    if value:
                        if isinstance(value, (int, float)):
                            value = six.text_type(value)
                        new_output.append(value)
                if new_output:
                    output += u' '.join(new_output) + u'\n'
        return output

    def get_text(self):
        workbook: Book = self._open_workbook()
        return self.extract_text(workbook)


class XlsReaderHandler(ProcessOpenHandler):

    def __init__(self, filepath):
        program = 'XlsReader'
        super(XlsReaderHandler, self).__init__(filepath, program, shell=False)



