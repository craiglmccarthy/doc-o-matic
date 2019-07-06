#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import tkinter as tk


def open_marc_folder():
    '''Opens folder to location of MARC files.'''
    os.system(r'start .\marc_files')


def join_marc_records(output_text):
    '''Joins MARC records located in MARC folder.'''
    # Change to MARC folder dir.
    os.chdir('./marc_files')
    marc_files = os.listdir()

    # Get number of MARC files, minus 1 from count if following file present.
    if 'combined_marc_files.mrc' in marc_files:
        num_marc_files = len(marc_files) - 1
    else:
        num_marc_files = len(marc_files)

    # If 2 or more files are present, join the contents into single file.
    if num_marc_files >= 2:
        with open('combined_marc_files.mrc', 'wb') as wfd:
            for f in marc_files:
                if f == 'combined_marc_files.mrc':
                    continue
                else:
                    with open(f, 'rb') as fd:
                        shutil.copyfileobj(fd, wfd)

        # Clear text box and provide status update.
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.INSERT, f'{str(num_marc_files)} MARC files were'
                           ' joined.\n')

    else:
        # Clear text box and provide status update.
        output_text.delete(1.0, tk.END)
        output_text.insert(
            tk.INSERT, 'At least two MARC records need to be present in the'
            ' the directory to join.\n')

    # Change dir back to root.
    os.chdir('..')


def submission(url_entry, output_text, document_request, output_to_text,
               output_to_marc, doc_regex):
    '''
    Requests document, searches document using regular expressions,
    outputs text to text box and writes data to a MARC file.
    '''

    # Function is True if tuple is returned.
    if document_request(url_entry, output_text):
        num_pages, document_output = document_request(url_entry, output_text)

        # Unpack tuples from doc_regex output.
        (doc_num, doc_year, doc_title, non_filing, _, _, doc_iss_year,
         welcomes, this_res, field_710, date_field_008, time_field_590,
         time_field_856) = doc_regex(document_output)

        # Outputs bibliographic data in text format to text field.
        output_to_text(output_text, doc_year, doc_num, non_filing, doc_title,
                       doc_iss_year, num_pages, welcomes, this_res,
                       date_field_008, time_field_590, field_710,
                       time_field_856, url_entry)

        # Outputs data in MARC format and writes to disk.
        output_to_marc(output_text, doc_year, doc_num, non_filing, doc_title,
                       doc_iss_year, num_pages, welcomes, this_res,
                       date_field_008, time_field_590, field_710,
                       time_field_856, url_entry)

        # Outputs string to text field.
        output_text.insert(
            tk.INSERT, '\n\nWriting to MARC file...')
    else:
        return
