#! /usr/bin/env python3
'''
Extract text from a PDF file.
'''

from pathlib import Path
from io import StringIO
import time


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import datasense as ds


def main():
    title_file_name_out = 'Name of txt file to save as?'
    title_file_name_in = 'Name of pdf file to read?'
    output_url = 'extract_text_from_pdf_file.html'
    file_types_out = [('txt files', '.txt .TXT')]
    file_types_in = [('pdf files', '.pdf .PDF')]
    header_title = 'Extract text from pdf file'
    header_id = 'extract-text-from-pdf-file'
    path_to_file_in = ds.ask_open_file_name_path(
        title=title_file_name_in,
        filetypes=file_types_in
    )
    path_to_file_out = ds.ask_save_as_file_name_path(
        title=title_file_name_out,
        filetypes=file_types_out
    )
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    start_time = time.time()
    string_with_lines = pdf_to_text(path=path_to_file_in)
    tidy = tidy_string(string=string_with_lines)
    save_to_file(
        path=path_to_file_out,
        string=tidy
    )
    stop_time = time.time()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False,
        read_file_names=path_to_file_in,
        save_file_names=path_to_file_out
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def save_to_file(
    path: Path,
    string: str
):
    '''
    Save a string to a file.
    '''
    file_to_save = open(
        file=path,
        mode='w'
    )
    file_to_save.write(string)


def tidy_string(string: str) -> str:
    '''
    Strip empty lines, leading spaces, trailing spaces from a string.
    '''
    lines = string.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    tidy = ''
    for line in non_empty_lines:
        tidy += line.strip() + '\n'
    return tidy


def pdf_to_text(path: Path) -> str:
    '''
    Extract all text from PDF file into a string.
    '''
    manager = PDFResourceManager()
    retstr = StringIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(
        manager,
        retstr,
        laparams=layout
    )
    filepath = open(
        file=path,
        mode='rb'
    )
    interpreter = PDFPageInterpreter(
        manager,
        device
    )
    for page in PDFPage.get_pages(
        filepath,
        check_extractable=True
    ):
        interpreter.process_page(page)
    text = retstr.getvalue()
    filepath.close()
    device.close()
    retstr.close()
    return text


if __name__ == "__main__":
    main()
