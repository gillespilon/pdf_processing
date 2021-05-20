#! /usr/bin/env python3
'''
Extract text from a PDF file.

- Create a directory for the pdf files
- Put all of the pdf files in this directory
- Create a directory for the txt files
- The output files will be in this directory
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
    # Define parameters
    title_directory_out = 'Name of the directory to save as?'
    title_directory_in = 'Name of the directory to read in?'
    output_url = 'extract_text_from_pdf_file.html'
    header_title = 'Extract text from pdf file'
    header_id = 'extract-text-from-pdf-file'
    extension_in = ['pdf', 'PDF']
    extension_out = '.txt'
    # Request file to read
    path_to_files_in = ds.ask_directory_path(
        title=title_directory_in,
        initialdir=Path.cwd()
    )
    # Request file to save
    path_to_files_out = ds.ask_directory_path(
        title=title_directory_out,
        initialdir=Path.cwd()
    )
    # Begin html output
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    start_time = time.time()
    list_raw_files = ds.directory_file_list(
        path=path_to_files_in,
        extension=extension_in
    )
    # Process pdf, save txt
    for item in list_raw_files:
        string_with_lines = pdf_to_text(path=item)
        tidy = tidy_string(string=string_with_lines)
        save_to_file(
            path=Path(path_to_files_out, f'{Path(item).stem}{extension_out}'),
            string=tidy
        )
    list_raw_file_names = [Path(item).name for item in list_raw_files]
    list_txt_file_names = [
        f'{Path(item).stem}{extension_out}' for item in list_raw_files
    ]
    stop_time = time.time()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    ds.print_list_by_item(
        list=list_raw_file_names,
        title='Files read:'
    )
    ds.print_list_by_item(
        list=list_txt_file_names,
        title='Files saved:'
    )
    # End html output
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

    Parameters
    ----------
    path : Path
        The file path.
    string : str
        The string to save in the file.

    Example
    -------
    >>> save_to_file(
    >>>     path=path_to_files_out,
    >>>     string=string
    >>> )
    '''
    file_to_save = open(
        file=path,
        mode='w'
    )
    file_to_save.write(string)


def tidy_string(string: str) -> str:
    '''
    Strip empty lines, leading spaces, trailing spaces from a string.

    Parameters
    ----------
    string : str
        The string to clean.

    Returns
    -------
    tidy : str
        The cleaned string.

    Example
    -------
    >>> tidy = tidy_string(string=string)
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

    Parameters
    ----------
    path : Path
        The path of the pdf file.

    Returns
    -------
    text : str
        The string of raw text from the pdf file.

    Example
    -------
    >>> string = pdf_to_text(path=path_to_files_in)
    '''
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(
        rsrcmgr,
        retstr,
        laparams=layout
    )
    filepath = open(
        file=path,
        mode='rb'
    )
    interpreter = PDFPageInterpreter(
        rsrcmgr,
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
